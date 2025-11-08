# LIRA - Lightweight Intelligent Reasoning Agent

LIRA is a lightweight, extensible framework for creating and managing AI agents. It is designed to be a simple, self-contained system that can be easily deployed and managed on a local machine.

## Features

*   **Simple API:** A basic API to interact with the LIRA core.
*   **Systemd Service:** Runs as a systemd service for easy management.
*   **Extensible:** Designed to be easily extended with new agents and capabilities.

## Installation

To install LIRA, run the installation script from the `scripts` directory:

```bash
./scripts/install.sh
```

This will install LIRA to `~/.lira` and set up a systemd service to run the LIRA API.

You can also use the `--yes` flag to run the installation in silent mode:

```bash
./scripts/install.sh --yes
```

## Usage

Once installed, the LIRA API will be running on `http://localhost:1312`. You can check the status of the service with:

```bash
sudo systemctl status lira.service
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
