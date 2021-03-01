# gisaid-uploader
 Simplified uploads to GISAID

Authenticate once: 

```python
    >>> import gisaid as gs
    >>> gs.GiSaid(authenticate=True, client_id='foo',
    >>>              username='bar', password='foobar', filename='authfile.json')
    Authentication successful
```

Usage:

```python
    >>> import gisaid as gs
    >>> files = ["authfile.json", "upload.csv", "fasta.fa"]
    >>> x = gs.GiSaid(files)
    >>> x.upload()
    "Upload successful"
```