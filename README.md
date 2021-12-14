# wifiqr

wifiqr is a utility that generates Wireless QR Code configurations for Android / iOS.
The QR Code produced can either be a Text (Unicode Characters) or an Image.


## Setting up

Install the packages listed on `requirements.txt` with the following command

```
pip install -r requirements.txt
```

Once that's done, you should be able to run the script by typing

```
python wifiqr.py
```

The binaries' names for `pip` and `python` may differ on different operating systems.
In that case, check on your system's documentation.


## TL;DR Usage

Most likely, the only set of options you may use are the following:

| Option           | Description                          |
| ----             | ----                                 |
| `-s, --ssid` ARG | Wi-Fi Name                           |
| `-k, --key`  ARG | Wi-Fi Password                       |
| `-h, --hidden`   | For hidden Wi-Fi AP, use this option |
| `-a, --auth` ARG | Encryption Protocol (default: WPA2)  |

For all options, you can run the script and pass `--help`. You may want to take a look
at the option `-t, --terminal` and `-o, --output` in case you are working solely with
the terminal or if you want to output to a file.


## Small heads up for Windows Users

I hardly, if ever, use Windows (nor I have computer with it), hence I haven't tested
there, which means this code might not be compatible with Windows. Kindly file an issue,
so I can fix any problems that may arise as soon as possible!


## Contributing

If you feel interested in contributing to the project, feel free to send a PR!
Granted that the additions are beneficial, I'll be merging them.

Bug fixes are also welcome, nobody writes perfect code anyway!


## Motivations

I was already annoyed by the fact that every time I wanted to connect a new device to
my network, I had to type the password. And adding up to that, I started to read up
on Python's documentation, then I came with an idea of creating my own simple QR Code
generator, so I wouldn't have to type the password every time and also would practice
a bit on my Python's skills.


## License

This project is licensed under the MIT License. See LICENSE for more information.

This project uses a third party library, [lincolnloop/python-qrcode](https://github.com/lincolnloop/python-qrcode),
you may want to check its license and its source code as well.

Also, the `.gitignore` file is provided by [toptal/gitignore](https://github.com/toptal/gitignore/).
