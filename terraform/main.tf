terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
  }

  provider "aws" {
    region  = var.aws_region
    profile = "marta"
  }

  data "aws_vpc" "default" {
    id = "vpc-02cd3181f43e5f18a"
  }

  resource "aws_internet_gateway" "igw" {
    vpc_id = data.aws_vpc.default.id

    tags = {
      Name = "youtube-devops-igw"
    }
  }

  resource "aws_route_table" "public" {
    vpc_id = data.aws_vpc.default.id

    route {
      cidr_block = "0.0.0.0/0"
      gateway_id = aws_internet_gateway.igw.id
    }

    tags = {
      Name = "youtube-devops-rt"
    }
  }

  resource "aws_route_table_association" "public" {
    subnet_id      = "subnet-0dcc0638fe99f01a0"
    route_table_id = aws_route_table.public.id
  }

  resource "aws_key_pair" "deployer" {
    key_name   = "youtube-devops-key"
    public_key = file("~/.ssh/id_ed25519.pub")
  }

  resource "aws_security_group" "youtube_sg" {
    name   = "youtube-devops-sg"
    vpc_id = data.aws_vpc.default.id

    ingress {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  resource "aws_instance" "youtube_server" {
    ami                         = var.ami_id
    instance_type               = var.instance_type
    key_name                    = aws_key_pair.deployer.key_name
    vpc_security_group_ids      = [aws_security_group.youtube_sg.id]
    subnet_id                   = "subnet-0dcc0638fe99f01a0"
    associate_public_ip_address = true

    tags = {
      Name    = "youtube-devops-platform"
      Project = "youtube-devops"
    }
  }