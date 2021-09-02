# IMDB Quick model serving - Keras version
To test the global models trained by FEDn, make sure to update the config params to minio.

```python
client = Minio('localhost:9000',
                  access_key='fedn_admin',
                  secret_key='password',
                  secure=False )
```
Start Flask App and choose the global models from the list:
```bash
python app.py
```
## License
Apache-2.0 (see LICENSE file for full information).