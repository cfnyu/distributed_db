# Parser Class
###### The Parser is a utility class used to parse a text file to be used by the application.

**USAGE:**

To use this class in code, use the following snippet:
    
```python    
parser = Parser()
parser.parse_file(sys.argv[1])
```

To test this class from the command line, execute the following command:
```python
python parser.py <input_file_path> -v
```

**Optional Parameter**

    The -v option should only be used for debugging. It sets the Verbose flag to true.
    Once set, all log statements will be printed
