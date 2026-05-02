import boto3

cloudfront = boto3.client('cloudfront')

def setup_cdn_caching():
    distribution_config = {
        'CallerReference': 'static-assets-cdn-1',
        'Aliases': {'Quantity': 0},
        'DefaultRootObject': 'index.html',
        'Origins': {
            'Quantity': 1,
            'Items': [{
                'Id': 'S3-Static-Bucket',
                'DomainName': 'my-assets-bucket.s3.amazonaws.com',
                'S3OriginConfig': {'OriginAccessIdentity': ''}
            }]
        },
        'DefaultCacheBehavior': {
            'TargetOriginId': 'S3-Static-Bucket',
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {'Forward': 'none'}
            },
            'TrustedSigners': {'Enabled': False, 'Quantity': 0},
            'ViewerProtocolPolicy': 'redirect-to-https',
            'MinTTL': 3600
        },
        'Enabled': True,
        'Comment': 'CDN for fast static asset delivery'
    }

    response = cloudfront.create_distribution(DistributionConfig=distribution_config)
    print(f"CDN Created: {response['Distribution']['DomainName']}")

if __name__ == "__main__":
    setup_cdn_caching()