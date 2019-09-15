from rest_framework.parsers import MultiPartParser
from rest_framework_csv.parsers import CSVParser


class CSVMultipartParser(MultiPartParser):
    """
    Parses CSV data from file attached as multipart form data.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        parser_context = parser_context or {}
        csv_file_field = parser_context.get('csv_file_field', 'csv_file')
        if csv_file_field not in data.files:
            return data
        file = data.files[csv_file_field]
        parsed_data = CSVParser().parse(file, parser_context=parser_context)
        return list(parsed_data)
