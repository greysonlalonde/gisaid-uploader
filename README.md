# gisaid-uploader
 Simplified uploads to GISAID
 - Meant for back-end integration, not cl

```python
    import gisaid as gs
    >>> files = ["gisaid_authfile.json", "upload.csv", "cov.fa"]
    >>> x = gs.GiSaid(files)
    >>> x.upload()
    "Upload successful"
```