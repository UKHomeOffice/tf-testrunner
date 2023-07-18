resource "aws_instance" "foo" {
  ami           = "foo"
  instance_type = "t2.micro"
}