terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "bernard-host-2580" 
  region  = "europe-north1"      
}

# Define a secure GCS bucket for data storage
resource "google_storage_bucket" "secure_bucket" {
  name                        = "helsinki-tech-project-bucket-2026"
  location                    = "EUROPE-NORTH1"
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true # Best practice security setting

  # Prevents accidental deletion of your infrastructure
  lifecycle {
    prevent_destroy = false # Change to true for real production systems
  }
}

# Output the URL of the created bucket
output "bucket_url" {
  value       = google_storage_bucket.secure_bucket.url
  description = "The direct URL of the created bucket"
}
