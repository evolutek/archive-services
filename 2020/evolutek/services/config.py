#!/usr/bin/env python3
from configparser import ConfigParser, NoSectionError, NoOptionError

from cellaserv.service import Service
from cellaserv.settings import make_setting
make_setting('CONFIG_FILE', '/etc/conf.d/config.ini', 'config', 'file', 'CONFIG_FILE')
from cellaserv.settings import CONFIG_FILE

class Config(Service):
    def __init__(self):
        self.config_file = ConfigParser()
        self.temporary_config = {}
        self.config_file.read([CONFIG_FILE, ])

        # Start the service
        super().__init__()

    @Service.action
    def get_section(self, name : str) -> dict:
        """
        Return section from config file. If the section does not exists, a
        KeyError is raised
        """

        tmp = {}

        if name in self.temporary_config:
            tmp = self.temporary_config[name]

        try:
            section = self.config_file.items(name)
            ret = {}
            for val in section:
              ret[val[0]] = val[1]


            for option in tmp:
                ret[option] = tmp[option]

            return ret

        except (NoSectionError) as exc:
            if tmp == {}:
                raise KeyError("Unknown config section: {0}".format(section)) from exc
            return tmp

    @Service.action
    def get(self, section: str, option: str) -> str:
        """
        Return value from config file. If the section does not exists, a
        KeyError is raised.
        """
        if section in self.temporary_config and option in self.temporary_config[section]:
            return self.temporary_config[section][option]

        try:
            return self.config_file.get(section, option)
        except (NoSectionError, NoOptionError) as exc:
            raise KeyError("Unknown config: {0}.{1}".format(section, option)) from exc

    @Service.action
    def set(self, section: str, option: str, value: str) -> None:
        """Write config value."""

        # Flush temporary value
        if section in self.temporary_config and option in self.temporary_config[section]:
            del self.temporary_config[section][option]

        try:
            self.config_file.set(section, option, value)
        except NoSectionError:
            self.config_file.add_section(section)
            self.config_file.set(section, option, value)

        # Publish update event
        self.publish('config.{0}.{1}'.format(section, option), value=value)

        self.write_config()

    def write_config(self):
        with open(CONFIG_FILE, "w") as f:
            self.config_file.write(f)

    @Service.action
    def set_tmp(self, section: str, option: str, value: str) -> None:
        """Set a temporary value."""
        if not section in self.temporary_config:
            self.temporary_config[section] = {}

        self.temporary_config[section][option] = value

    @Service.action
    def write(self) -> None:
        """Write temporary config to file."""
        for section in self.temporary_config:
            for option, value in self.temporary_config[section].items():

                # We can't use self.set() because it modifies self.temporary_config
                try:
                    self.config_file.set(section, option, value)
                except NoSectionError:
                    self.config_file.add_section(section)
                    self.config_file.set(section, option, value)

        self.write_config()
        self.temporary_config.clear()

    @Service.action
    def list(self) -> str:
        """Get the content of the config file."""
        ret = {}
        for section in self.config_file.sections():
            ret[section] = {}
            for k, v in self.config_file.items(section):
                ret[section][k] = v
        return ret

def main():
    config = Config()
    config.run()

if __name__ == '__main__':
    main()
