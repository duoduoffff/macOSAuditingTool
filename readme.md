# macOS Auditing tool

This is a command-line tool that enables you to save or print (on paper!) information of your macOS device. It does so by utilizing some of your builtin cli tools, and prints the result directly to white paper.

It is suggested you have a dot matrix printer for best experience.

Save the evidence and prevent repudiation!

This tool currently supports:

- Listing software packages (pkgutil)
- Listing brew packages
- Listing TTY login history
- Listing sudo history (via terminal)
- Listing Keychain access log
- Listing lock and unlock history
- Specify important files and folders and print out their sizes (configurable via json config file)
- Listing iCloud information
- Listing Bilibili play history
- Listing Bilibili login attempts (recent week only)
- Listing 3rd-party kexts

Feature plans:

[x] Support printing. (v1.0)
[] Command line bug fixes. (v1.1)
[x] Modify logic to support time filter for bilibili history. (v1.0)
[] Implement OpenPGP to sign every print, so that the print log can be reversibly looked up so there is no place for forged lookups. (v1.3)


## Contribute!

If you have got anything to point out or you'd like to submit code, feel free to open a pull request.
