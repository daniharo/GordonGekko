# Priority Matrix API test: GordonGekko

This test uses the `yfinance` package to check if a given ticker is going down in price,
then adding an item in Priority Matrix as a reminder that you should sell shares.

Before executing `main.py` you must add an `auth.py` file with the following content:

```python
auth = {
    "email": "Your email registered in appfluence",
    "token": "Token obtained from https://prioritymatrix.com/o/authorized_tokens/"
}
```
