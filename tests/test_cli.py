from das_opendata_analysis.cli import build_parser


def test_parser_defaults() -> None:
    args = build_parser().parse_args([])
    assert args.path.as_posix() == "data/raw"
    assert args.output.as_posix() == "outputs/inventory.csv"
    assert args.no_update is False
