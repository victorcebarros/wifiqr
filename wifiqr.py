"""Generate QR Code for Android / iOS WLAN Setup.

Copyright (c) 2021 Victor Cebarros

This file is part of wifiqr. It is licensed under the
MIT License. See README.md and LICENSE for more info.
"""

import argparse
import io
import os
import sys

import qrcode  # type: ignore


EXIT_SUCCESS = 0
EXIT_FAILURE = 1

USAGE = """\
usage: {} [OPTIONS]

Generate Wi-Fi Network QR Code

OPTIONS
  -s, --ssid SSID
    Sets Wireless Network Name (SSID)

  -k, --key KEY
    Sets Password

  -a, --auth WEP|WPA|WPA2|WPA2-EAP|nopass
    Sets Encryption Protocol (defaults to WPA2)

  -h, --hidden
    Sets whether Network is hidden or not

  -o, --output PATH
    Outputs image to PATH

    If output option not passed, an image of
    the QR Code will be shown to the screen
    unless overriden by -t option.

  -t, --terminal
    Outputs a text version to terminal instead
    of a picture.

    Useful when working with TTYs or maybe
    you just want the text version.

  --help
    Displays this help text and then exits

ADVANCED OPTIONS:
  -e, --eap-method PEAP|TLS|TTLS|PWD|SIM|AKA|AKA'|...
  -p, --ph2 MSCHAPV2|GTC|SIM|AKA|AKA'|...
  -i, --identity IDENTITY
  -A, --anonymous-identity IDENTITY"""


def parse_argv(argv: list) -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(usage=USAGE, add_help=False,
                                     allow_abbrev=False)
    parser.add_argument("-s", "--ssid")
    parser.add_argument("-k", "--key")
    parser.add_argument("-a", "--auth", default="WPA2")
    parser.add_argument("-h", "--hidden", action="store_true")
    parser.add_argument("-o", "--output")
    parser.add_argument("-t", "--terminal", action="store_true")
    parser.add_argument("-e", "--eap-method")
    parser.add_argument("-p", "--ph2")
    parser.add_argument("-i", "--identity")
    parser.add_argument("-A", "--anonymous-identity")
    parser.add_argument("--help", action="store_true")

    return parser.parse_args(argv[1:])


def escape(pattern: str, special_chars: bytes = b"\\;,\":") -> str:
    """Escape special characters in a string.

    This is an adaptation from Python's own re library.
    See more at:
    https://github.com/python/cpython/blob/3.10/Lib/re.py#L269-L277
    """
    return pattern.translate({c: "\\" + chr(c) for c in special_chars})


def gen_wifi_str(*, ssid: str = None, key: str = None, auth: str = None,
                 hidden: bool = False, eap: str = None, ph2: str = None,
                 identity: str = None, anonidentity: str = None) -> str:
    """Generates Wi-Fi String for QR Code.

    More information on how this string works can be found at
    https://github.com/zxing/zxing/wiki/Barcode-Contents
    """
    wifi_str = "WIFI:"

    def param(par, arg):
        return "" if arg is None else f"{par}:{escape(arg)};"

    wifi_str += param("T", auth)
    wifi_str += param("S", ssid)
    wifi_str += param("P", key)
    wifi_str += param("H", str(hidden).lower())
    wifi_str += param("E", eap)
    wifi_str += param("A", anonidentity)
    wifi_str += param("I", identity)
    wifi_str += param("PH2", ph2)
    wifi_str += ";"

    return wifi_str


def prompt(*, msg: str = None, opts: dict[str, bool] = None) -> bool:
    """Prompts user with message and then performs action accordingly.

    NOTE: Opts are case insensitive!
    """
    answer = ""

    if opts is None:
        opts = {"y": True, "ye": True, "yes": True, "n": False, "no": False}

    while (answer := input(msg).lower()) not in opts:
        pass

    return opts[answer]


def can_overwrite(outfile: str) -> bool:
    """Prompts if user wants to overwrite file."""
    if os.path.exists(outfile):
        msg = f"Are you sure you want to overwrite \"{outfile}\"? [y|n] "
        return prompt(msg=msg)

    return True


def gen_wifi_qr(wifi_str: str, outfile: str = None,
                is_terminal: bool = False) -> None:
    """Generates Wi-Fi QR, and outputs to the screen or to a file."""
    code = qrcode.QRCode()
    code.add_data(wifi_str)

    if is_terminal:
        buffer = io.StringIO()
        code.print_ascii(out=buffer, invert=True)
        qrstring = buffer.getvalue()
        buffer.close()

        if outfile is None:
            print(qrstring, end="")
            return

        with open(outfile, "w", encoding="utf-8") as out:
            out.write(qrstring)
            return

    img = code.make_image()

    if outfile is None:
        img.show()
        return

    img.save(outfile)


def main(argv: list) -> int:
    """Entry point."""
    options = parse_argv(argv)

    if len(argv) < 2 or options.help:
        print(USAGE.format(argv[0]), file=sys.stderr)
        return EXIT_FAILURE

    wifi_str = gen_wifi_str(ssid=options.ssid, key=options.key,
                            auth=options.auth, hidden=options.hidden,
                            eap=options.eap_method, ph2=options.ph2,
                            identity=options.identity,
                            anonidentity=options.anonymous_identity)

    print("Created", wifi_str)

    auth = {"WEP", "WPA", "WPA2", "WPA2-EAP"}
    if not options.key and options.auth.upper() in auth:
        print("warning: Wi-Fi connection is missing a password!",
              file=sys.stderr)

    if options.output and not can_overwrite(options.output):
        print("error: User refused to overwrite:",
              options.output, file=sys.stderr)
        return EXIT_FAILURE

    try:
        gen_wifi_qr(wifi_str, options.output, options.terminal)
    except (ValueError, OSError) as err:
        print("error: Could not save file:", err, file=sys.stderr)
        return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main(sys.argv))
