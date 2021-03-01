# gisaid-uploader
 Simplified uploads to GISAID


```python
    >>> import gisaid as gs
    >>> files = ["gisaid_authfile.json", "upload.csv", "cov.fa"]
    >>> x = gs.GiSaid(files)
    >>> x.upload()
    "Upload successful"
```
