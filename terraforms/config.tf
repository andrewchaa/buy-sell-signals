terraform {
  backend "s3" {
    bucket = "deepeyes-terraform-resources"
    key    = "decide-buy-sell"
    region = "eu-west-1"
  }
  required_version = "~>1.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.40"
    }
  }
}
