output "server_ip" {
    value = aws_instance.youtube_server.public_ip
  }

  output "server_dns" {
    value = aws_instance.youtube_server.public_dns
  }