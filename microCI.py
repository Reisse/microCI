#!/usr/bin/python3


import argparse
import configparser

import micro_ci.deployment


def main():
    parser = argparse.ArgumentParser(description='Simple CI/CD.')
    parser.add_argument('-d', '--deployments', metavar='FILE', help='file with the configuration of the deployments')
    parser.add_argument('-i', '--immediate', action='store_true', help='execute the first deployment immediately')
    args = parser.parse_args()

    if args.deployments:
        config = configparser.ConfigParser({ 'sha' : '', 'immediate' : 'False' })
        config.read(args.deployments)

        for deployment in config.sections():
            if args.immediate:
                config[deployment]['immediate'] = 'True'

            micro_ci.deployment.schedule_deployment(config[deployment])


if __name__ == '__main__':
    main()
