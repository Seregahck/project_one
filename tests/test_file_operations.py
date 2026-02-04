import pytest
import pandas as pd
from unittest.mock import mock_open, patch, MagicMock
from src.file_operations import read_csv_transactions, read_excel_transactions


class TestReadCSVTransactions:
    """Тесты для функции read_csv_transactions"""

    def test_read_csv_transactions_success(self):
        """Тест успешного чтения CSV файла"""
        # Подготавливаем тестовые данные
        csv_content = """date,amount,category,description
2023-10-01,1000.50,Salary,Monthly salary
2023-10-02,-50.00,Groceries,Supermarket
2023-10-03,-25.00,Transport,Bus ticket"""

        # Мокаем open и csv.DictReader
        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('csv.DictReader') as mock_reader:
                # Настраиваем mock для DictReader
                mock_reader_instance = MagicMock()
                mock_reader_instance.fieldnames = ['date', 'amount', 'category', 'description']
                mock_reader_instance.__iter__.return_value = [
                    {
                        'date': '2023-10-01',
                        'amount': '1000.50',
                        'category': 'Salary',
                        'description': 'Monthly salary'
                    },
                    {
                        'date': '2023-10-02',
                        'amount': '-50.00',
                        'category': 'Groceries',
                        'description': 'Supermarket'
                    },
                    {
                        'date': '2023-10-03',
                        'amount': '-25.00',
                        'category': 'Transport',
                        'description': 'Bus ticket'
                    }
                ]
                mock_reader.return_value = mock_reader_instance

                # Вызываем тестируемую функцию
                result = read_csv_transactions('dummy_path.csv')

                # Проверяем результаты
                assert len(result) == 3
                assert result[0]['date'] == '2023-10-01'
                assert result[0]['amount'] == '1000.50'
                assert result[0]['category'] == 'Salary'
                assert result[1]['amount'] == '-50.00'
                assert result[2]['category'] == 'Transport'

    def test_read_csv_transactions_empty_values(self):
        """Тест чтения CSV с пустыми значениями"""
        csv_content = """date,amount,category,description
2023-10-01,1000.50,Salary,
2023-10-02,,Groceries,Supermarket"""

        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('csv.DictReader') as mock_reader:
                mock_reader_instance = MagicMock()
                mock_reader_instance.fieldnames = ['date', 'amount', 'category', 'description']
                mock_reader_instance.__iter__.return_value = [
                    {
                        'date': '2023-10-01',
                        'amount': '1000.50',
                        'category': 'Salary',
                        'description': ''
                    },
                    {
                        'date': '2023-10-02',
                        'amount': '',
                        'category': 'Groceries',
                        'description': 'Supermarket'
                    }
                ]
                mock_reader.return_value = mock_reader_instance

                result = read_csv_transactions('dummy_path.csv')

                assert result[0]['description'] is None
                assert result[1]['amount'] is None

    def test_read_csv_transactions_file_not_found(self):
        """Тест ошибки при отсутствии файла"""
        with pytest.raises(FileNotFoundError):
            read_csv_transactions('non_existent_file.csv')

    def test_read_csv_transactions_empty_file(self):
        """Тест ошибки при пустом файле"""
        csv_content = ""

        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('csv.DictReader') as mock_reader:
                mock_reader_instance = MagicMock()
                mock_reader_instance.fieldnames = None
                mock_reader.return_value = mock_reader_instance

                with pytest.raises(ValueError, match="CSV файл пуст или не содержит заголовков"):
                    read_csv_transactions('empty.csv')

    def test_read_csv_transactions_no_data(self):
        """Тест ошибки при отсутствии данных"""
        csv_content = "date,amount,category,description"

        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('csv.DictReader') as mock_reader:
                mock_reader_instance = MagicMock()
                mock_reader_instance.fieldnames = ['date', 'amount', 'category', 'description']
                mock_reader_instance.__iter__.return_value = []
                mock_reader.return_value = mock_reader_instance

                with pytest.raises(ValueError, match="CSV файл не содержит данных"):
                    read_csv_transactions('only_headers.csv')


class TestReadExcelTransactions:
    """Тесты для функции read_excel_transactions"""

    def test_read_excel_transactions_success(self):
        """Тест успешного чтения Excel файла"""
        # Создаем mock DataFrame
        mock_data = [
            {'date': '2023-10-01', 'amount': 1000.50, 'category': 'Salary', 'description': 'Monthly salary'},
            {'date': '2023-10-02', 'amount': -50.00, 'category': 'Groceries', 'description': 'Supermarket'},
            {'date': '2023-10-03', 'amount': -25.00, 'category': 'Transport', 'description': 'Bus ticket'}
        ]
        mock_df = pd.DataFrame(mock_data)

        # Патчим pd.read_excel
        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = mock_df

            # Вызываем тестируемую функцию
            result = read_excel_transactions('dummy_path.xlsx')

            # Проверяем результаты
            assert len(result) == 3
            assert result[0]['date'] == '2023-10-01'
            assert result[0]['amount'] == 1000.50
            assert result[0]['category'] == 'Salary'
            assert result[1]['amount'] == -50.00
            assert result[2]['category'] == 'Transport'


    def test_read_excel_transactions_file_not_found(self):
        """Тест ошибки при отсутствии файла"""
        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.side_effect = FileNotFoundError("File not found")

            with pytest.raises(FileNotFoundError):
                read_excel_transactions('non_existent_file.xlsx')

    def test_read_excel_transactions_empty_file(self):
        """Тест ошибки при пустом файле"""
        # Создаем пустой DataFrame
        mock_df = pd.DataFrame()

        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = mock_df

            with pytest.raises(ValueError, match="Excel файл пуст"):
                read_excel_transactions('empty.xlsx')

    def test_read_excel_transactions_with_sheet_name(self):
        """Тест чтения определенного листа Excel"""
        mock_data = [
            {'date': '2023-10-01', 'amount': 1000.50, 'category': 'Salary'}
        ]
        mock_df = pd.DataFrame(mock_data)

        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = mock_df

            # Тестируем с указанием имени листа
            result = read_excel_transactions('dummy_path.xlsx', sheet_name='Transactions')

            # Проверяем, что read_excel был вызван с правильными параметрами
            mock_read_excel.assert_called_once_with('dummy_path.xlsx', sheet_name='Transactions')
            assert len(result) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])