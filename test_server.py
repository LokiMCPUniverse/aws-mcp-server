#!/usr/bin/env python3
"""Test script for AWS MCP Server"""

import sys
import json
from src.aws_mcp.config import AWSConfig
from src.aws_mcp.client import AWSClient

def test_config():
    """Test configuration loading"""
    print("Testing AWS MCP Server configuration...")
    
    try:
        config = AWSConfig()
        print("✓ Configuration loaded successfully")
        
        # Check if credentials are available
        has_keys = all([config.access_key_id, config.secret_access_key])
        has_profile = config.profile is not None
        has_role = config.role_arn is not None
        
        print(f"  - Access Keys: {'✓' if has_keys else '✗'}")
        print(f"  - AWS Profile: {'✓' if has_profile else '✗'} ({config.profile if has_profile else 'None'})")
        print(f"  - IAM Role: {'✓' if has_role else '✗'}")
        print(f"  - Default Region: {config.default_region}")
        
        return config
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return None

def test_client(config):
    """Test AWS client initialization"""
    print("\nTesting AWS Client initialization...")
    
    try:
        account_config = config.get_account_config()
        region_config = config.get_region_config()
        cost_config = config.get_cost_config()
        
        client = AWSClient(account_config, region_config, cost_config)
        print("✓ AWS Client initialized successfully")
        
        # Test basic operations
        print("\nTesting basic AWS operations...")
        
        # List S3 buckets (requires valid credentials)
        try:
            buckets = client.list_buckets()
            print(f"✓ Listed {len(buckets)} S3 buckets")
        except Exception as e:
            print(f"✗ S3 list buckets failed: {e}")
        
        return client
    except Exception as e:
        print(f"✗ Client initialization error: {e}")
        return None

def main():
    """Main test function"""
    print("AWS MCP Server Test Suite")
    print("=" * 50)
    
    # Test configuration
    config = test_config()
    if not config:
        print("\n⚠️  Configuration test failed. Server cannot start without valid AWS credentials.")
        print("\nTo fix this, you need to:")
        print("1. Set AWS credentials in the .env file, OR")
        print("2. Configure AWS credentials using 'aws configure', OR")
        print("3. Set AWS environment variables")
        return 1
    
    # Test client
    client = test_client(config)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"- Configuration: {'✓' if config else '✗'}")
    print(f"- Client: {'✓' if client else '✗'}")
    
    if config and client:
        print("\n✓ AWS MCP Server appears to be working correctly!")
        print("  The server can be started with: python -m aws_mcp.server")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
    
    return 0 if (config and client) else 1

if __name__ == "__main__":
    sys.exit(main())