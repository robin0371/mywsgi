import click.testing

from mywsgi.__main__ import main


class TestMain:

    def test_ok(self, app, mocker):
        mock_app_import = mocker.patch("mywsgi.__main__.import_app", return_value=app)
        mock_server = mocker.Mock()
        mock_server.serve_forever = mocker.MagicMock()
        mock_make_server = mocker.patch("mywsgi.__main__.make_server", return_value=mock_server)

        runner = click.testing.CliRunner()
        result = runner.invoke(main, ["my_test_mywsgi_module:app", "localhost", "8383"])

        assert result.exit_code == 0
        mock_app_import.assert_called_once_with("my_test_mywsgi_module:app")
        mock_make_server.assert_called_once_with(app, "localhost", 8383)
        assert mock_server.serve_forever.call_count == 1

    def test_import_app_error(self, app, mocker):
        mock_app_import = mocker.patch("mywsgi.__main__.import_app", side_effect=ImportError)
        mock_server = mocker.Mock()
        mock_server.serve_forever = mocker.MagicMock()
        mock_make_server = mocker.patch("mywsgi.__main__.make_server", return_value=mock_server)

        runner = click.testing.CliRunner()
        result = runner.invoke(main, ["my_test_mywsgi_module:app", "localhost", "8383"])

        assert result.exit_code == 0
        mock_app_import.assert_called_once_with("my_test_mywsgi_module:app")
        assert mock_make_server.call_count == 0
        assert mock_server.serve_forever.call_count == 0

    def test_make_server_error(self, app, mocker):
        mock_app_import = mocker.patch("mywsgi.__main__.import_app", return_value=app)
        mock_server = mocker.Mock()
        mock_server.serve_forever = mocker.MagicMock()
        mock_make_server = mocker.patch("mywsgi.__main__.make_server", side_effect=TypeError)

        runner = click.testing.CliRunner()
        result = runner.invoke(main, ["my_test_mywsgi_module:app", "localhost", "8383"])

        assert result.exit_code == 0
        mock_app_import.assert_called_once_with("my_test_mywsgi_module:app")
        mock_make_server.assert_called_once_with(app, "localhost", 8383)
        assert mock_server.serve_forever.call_count == 0

    def test_server_error(self, app, mocker):
        mock_app_import = mocker.patch("mywsgi.__main__.import_app", return_value=app)
        mock_server = mocker.Mock()
        mock_server.serve_forever = mocker.MagicMock(side_effect=ValueError)
        mock_make_server = mocker.patch("mywsgi.__main__.make_server", return_value=mock_server)

        runner = click.testing.CliRunner()
        result = runner.invoke(main, ["my_test_mywsgi_module:app", "localhost", "8383"])

        assert result.exit_code == 0
        mock_app_import.assert_called_once_with("my_test_mywsgi_module:app")
        mock_make_server.assert_called_once_with(app, "localhost", 8383)
        assert mock_server.serve_forever.call_count == 1
