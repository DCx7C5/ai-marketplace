---
name: linux-forensic-disk-filecarving-photorec-detect
description: - When recovering deleted files from a forensic disk image or storage device - When the file system is corrupted, formatted, or overwritten - During investigations requiring recovery of documents, images, videos, or databases - When file system metadata is unavailable but raw data sectors remain intact - For recovering files from memory cards, USB 
domain: cybersecurity
---
------|-------------|
| File carving | Recovering files from raw data using file header/footer signatures |
| File signatures | Magic bytes at the start of files identifying their type (e.g., FF D8 FF for JPEG) |
| Unallocated space | Disk sectors not assigned to any active file; may contain deleted data |
| Fragmented files | Files stored in non-contiguous sectors; harder to carve completely |
| Cluster/Block size | Minimum allocation unit on a file system; affects carving granularity |
| File footer | Byte sequence marking the end of a file (not all formats have footers) |
| Data remanence | Residual data remaining after deletion until sectors are overwritten |
| False positives | Carved artifacts that match signatures but contain corrupted or partial data |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| PhotoRec | Open-source file carving tool supporting 300+ file formats |
| TestDisk | Companion tool for partition recovery and repair |
| Foremost | Alternative file carver originally developed by US Air Force OSI |
| Scalpel | High-performance file carver based on Foremost |
| hashdeep | Recursive hash computation and audit tool |
| jpeginfo | JPEG file integrity verification |
| file | Unix utility identifying file types by magic bytes |
| exiftool | Extract metadata from recovered image and document files |

## Common Scenarios

**Scenario 1: Recovering Deleted Evidence from a Suspect's USB Drive**
Image the USB drive with dcfldd, run PhotoRec targeting document and image formats, organize by file type, hash all recovered files, compare against known-bad hash sets, extract metadata from images for GPS and timestamp information.

**Scenario 2: Formatted Hard Drive Recovery**
Run PhotoRec in "Whole" mode against the entire formatted partition, recover all file types, expect higher false positive rate due to file fragmentation, validate recovered files with signature checking, catalog and hash for evidence chain.

**Scenario 3: Memory Card from a Surveillance Camera**
Recover deleted video files (AVI, MP4, MOV) from the memory card image, use targeted file type selection to speed recovery, verify video files are playable, extract frame timestamps, document recovery in case notes.

**Scenario 4: Corrupted File System on Evidence Drive**
When file system metadata is destroyed, PhotoRec bypasses the file system entirely and carves from raw sectors, recover maximum possible data, accept that file names and directory structure will be lost, rename files based on content during review.

## Output Format

```
PhotoRec Recovery Summary:
  Source Image:     evidence.dd (500 GB)
  Partition:        NTFS (Partition 2)
  Scan Mode:        Free space only

  Files Recovered:  4,523
    Documents:      234 (doc: 45, docx: 89, pdf: 67, xlsx: 33)
    Images:         2,145 (jpg: 1,890, png: 198, gif: 57)
    Videos:         34 (mp4: 22, avi: 12)
    Archives:       67 (zip: 45, rar: 22)
    Databases:      12 (sqlite: 8, dbf: 4)
    Other:          2,031

  Data Recovered:   12.4 GB
  Corrupted Files:  312 (flagged for review)
  Output Directory: /cases/case-2024-001/recovered/all/
  Hash Manifest:    /cases/case-2024-001/recovered/recovered_hashes.txt
```