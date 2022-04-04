try:
    from main import app
    import unittest

except Exception as e:
    print("Some Modules are Missing {}".format(e))

class FlaskTest(unittest.TestCase):
# Check For The Response 200
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get("/")
        statuscode=response.status_code
        self.assertEqual(statuscode, 200)

# Check if the content return is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/API")
        self.assertEqual(response.content_type, "application/json")



if __name__ == "__main__":
    unittest.main()