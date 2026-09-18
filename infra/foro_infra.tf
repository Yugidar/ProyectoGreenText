cat > infra/foro_infra.tf <<'EOF'
provider "aws" {
  region = "us-east-1"
}

# 1. Bucket S3 (Privado y Cifrado)
resource "aws_s3_bucket" "foro_bucket" {
  bucket = "greentext-s3"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "foro_crypto" {
  bucket = aws_s3_bucket.foro_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "foro_bloqueo" {
  bucket                  = aws_s3_bucket.foro_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 2. Base de Datos RDS (Cifrada y sin acceso publico)
resource "aws_db_instance" "foro_db" {
  identifier             = "foro-db"
  engine                 = "mysql"
  instance_class         = "db.t2.micro"
  allocated_storage      = 20
  storage_encrypted      = true
  publicly_accessible    = false
  skip_final_snapshot    = true
}
EOF
