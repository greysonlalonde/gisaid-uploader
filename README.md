# gisaid-uploader
 Simplified uploads to GISAID

1. Register for a [GISAID](https://www.gisaid.org/registration/register/) account

2. Email GISAID & request a client ID

Authenticate once: 

```python
    >>> import gisaid as gs
    >>> gs.GiSaid(authenticate=True, client_id='foo',
    >>>              username='bar', password='foobar', filename='authfile.json')
    "Authentication successful"
```


CSV + fasta file:

```python
    >>> import gisaid as gs
    >>> files = ["upload.csv", "fasta.fa"]
    >>> x = gs.GiSaid(files)
    >>> x.upload()
    "Upload successful"
```


Collated CSV:

```python
    >>> import gisaid as gs
    >>> files = ["collated", "upload.csv"]
    >>> x = gs.GiSaid(files)
    >>> x.upload()
    "Upload successful"
```
