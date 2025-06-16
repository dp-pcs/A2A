#!/bin/bash

# A2A Demo Deployment Script for LatentGenius.ai
# This script deploys the A2A dashboard to AWS S3 + CloudFront

set -e

echo "🚀 Deploying LatentGenius A2A Demo..."

# Configuration
DOMAIN="demo.latentgenius.ai"
S3_BUCKET="latentgenius-a2a-demo"
REGION="us-east-1"
DISTRIBUTION_ID=""

# Create S3 bucket for static hosting
echo "📦 Creating S3 bucket..."
aws s3 mb s3://$S3_BUCKET --region $REGION || true

# Configure bucket for static website hosting
aws s3 website s3://$S3_BUCKET \
    --index-document index.html \
    --error-document index.html

# Set bucket policy for public read access
cat > bucket-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$S3_BUCKET/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy --bucket $S3_BUCKET --policy file://bucket-policy.json

# Upload frontend files
echo "📤 Uploading frontend files..."
aws s3 sync ../frontend/ s3://$S3_BUCKET/ \
    --delete \
    --cache-control "public, max-age=86400"

# Create CloudFront distribution
echo "🌐 Creating CloudFront distribution..."
cat > cloudfront-config.json << EOF
{
    "CallerReference": "a2a-demo-$(date +%s)",
    "Aliases": {
        "Quantity": 1,
        "Items": ["$DOMAIN"]
    },
    "DefaultRootObject": "index.html",
    "Comment": "LatentGenius A2A Demo",
    "Enabled": true,
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "S3Origin",
                "DomainName": "$S3_BUCKET.s3-website-$REGION.amazonaws.com",
                "CustomOriginConfig": {
                    "HTTPPort": 80,
                    "HTTPSPort": 443,
                    "OriginProtocolPolicy": "http-only"
                }
            }
        ]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "S3Origin",
        "ViewerProtocolPolicy": "redirect-to-https",
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        },
        "ForwardedValues": {
            "QueryString": false,
            "Cookies": {
                "Forward": "none"
            }
        },
        "MinTTL": 0,
        "DefaultTTL": 86400,
        "MaxTTL": 31536000,
        "Compress": true
    },
    "ViewerCertificate": {
        "CloudFrontDefaultCertificate": true
    },
    "CustomErrorResponses": {
        "Quantity": 1,
        "Items": [
            {
                "ErrorCode": 404,
                "ResponsePagePath": "/index.html",
                "ResponseCode": "200",
                "ErrorCachingMinTTL": 300
            }
        ]
    }
}
EOF

# Get SSL certificate ARN (you'll need to request this first)
CERT_ARN=$(aws acm list-certificates --region us-east-1 \
    --query "CertificateSummaryList[?DomainName=='*.latentgenius.ai'].CertificateArn" \
    --output text)

if [ -n "$CERT_ARN" ]; then
    echo "🔒 Using SSL certificate: $CERT_ARN"
    # Update CloudFront config to use ACM certificate
    jq --arg cert "$CERT_ARN" '.ViewerCertificate = {
        "ACMCertificateArn": $cert,
        "SSLSupportMethod": "sni-only",
        "MinimumProtocolVersion": "TLSv1.2_2021"
    }' cloudfront-config.json > cloudfront-config-ssl.json
    mv cloudfront-config-ssl.json cloudfront-config.json
fi

# Create distribution
DISTRIBUTION_ID=$(aws cloudfront create-distribution \
    --distribution-config file://cloudfront-config.json \
    --query 'Distribution.Id' --output text)

echo "☁️ CloudFront Distribution ID: $DISTRIBUTION_ID"

# Wait for distribution to deploy
echo "⏳ Waiting for CloudFront distribution to deploy (this may take 10-15 minutes)..."
aws cloudfront wait distribution-deployed --id $DISTRIBUTION_ID

# Get CloudFront domain name
CLOUDFRONT_DOMAIN=$(aws cloudfront get-distribution --id $DISTRIBUTION_ID \
    --query 'Distribution.DomainName' --output text)

echo "🎉 Deployment complete!"
echo "📊 Dashboard URL: https://$CLOUDFRONT_DOMAIN"
echo "🌐 Custom Domain: https://$DOMAIN (configure DNS)"

# DNS Configuration Instructions
echo ""
echo "🔧 DNS Configuration:"
echo "Add this CNAME record to your Route 53 hosted zone:"
echo "Name: demo"
echo "Type: CNAME"
echo "Value: $CLOUDFRONT_DOMAIN"

# Create Route 53 record (if hosted zone exists)
HOSTED_ZONE_ID=$(aws route53 list-hosted-zones \
    --query "HostedZones[?Name=='latentgenius.ai.'].Id" \
    --output text | cut -d'/' -f3)

if [ -n "$HOSTED_ZONE_ID" ]; then
    echo "🚀 Creating Route 53 DNS record..."
    
    cat > dns-change.json << EOF
{
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "$DOMAIN",
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "$CLOUDFRONT_DOMAIN"
                    }
                ]
            }
        }
    ]
}
EOF

    aws route53 change-resource-record-sets \
        --hosted-zone-id $HOSTED_ZONE_ID \
        --change-batch file://dns-change.json

    echo "✅ DNS record created! Demo will be available at https://$DOMAIN in a few minutes."
else
    echo "⚠️  Route 53 hosted zone not found. Please create DNS record manually."
fi

# Cleanup
rm -f bucket-policy.json cloudfront-config.json dns-change.json

echo ""
echo "💰 Estimated monthly cost: $5-15"
echo "🔄 To update: Just run this script again to sync new files"
echo ""
echo "🎯 Next steps:"
echo "1. Visit https://$DOMAIN to see your demo"
echo "2. Deploy backend APIs for real A2A functionality"
echo "3. Update dashboard.js to connect to real backend" 