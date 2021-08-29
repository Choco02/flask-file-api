# A simple file upload API

* You send a file passing it (txt, pdf, png, jpg, jpeg, gif) at `/` using **POST** (for now only a single file) and you receive a file URL
* You can get the file accessing `/<filename.ext>` using **GET**

### Example

*If you are running project on your machine using default PORT (5000)*

**Sending a file**
```sh
$ curl -F 'file=@path/to/file.jpg' http://localhost:5000/
```

**Getting a file to your machine**
```sh
$ curl -o name.jpg http://localhost:5000/2474216.jpg
```

# How to run it
* Use Python's 3 pip
`pip install -r requirements.txt`
* Run `flask run`

# Run the tests
* `python3 run_tests.py` on Linux
* `python run_tests.py` on Windows

# TODO
- [x] Add tests
- [ ] Handle multiple files
