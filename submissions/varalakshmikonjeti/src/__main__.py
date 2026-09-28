import json
import sys

from .request_parser import parse_verification_request
from .runner import PackManagerRunner


def main() -> int:
    """
    Run the Pack Manager headless agent from standard input.

    Expected input is one JSON verification request.
    The structured decision is written to standard output.
    """
    try:
        raw_input = sys.stdin.read().strip()

        if not raw_input:
            print(
                json.dumps(
                    {
                        "error": "No verification request was provided."
                    },
                    indent=2,
                )
            )
            return 1

        payload = json.loads(raw_input)

        request = parse_verification_request(payload)

        runner = PackManagerRunner()

        result = runner.run(request)

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            )
        )

        return 0

    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {
                    "error": "Invalid JSON input.",
                    "details": str(exc),
                },
                indent=2,
            )
        )
        return 1

    except Exception as exc:
        print(
            json.dumps(
                {
                    "error": "Pack Manager execution failed.",
                    "details": str(exc),
                },
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())