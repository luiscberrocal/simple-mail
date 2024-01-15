import os
import sys
from pathlib import Path
from typing import List, Any, Dict

import click
from pydantic import ValidationError
from rich.pretty import pprint

from invoicing_tools.email.enums import EmailFormat
from invoicing_tools.email.mailer import send_email
from invoicing_tools.email.models import SenderConfig, EmailMessage
from invoicing_tools.exceptions import ConfigurationError
from invoicing_tools.naming import get_invoice_info_from_filename


def load_gmail_environment_variables():
    from dotenv import load_dotenv
    from pathlib import Path
    environment_folder = Path(__file__).parent.parent.parent / '.envs'
    environment_file = environment_folder / 'env.txt'
    if not environment_file.exists():
        error_message = f'Environment file {environment_file} not found.'
        raise ConfigurationError(error_message)
    dotenv_path = Path(environment_file)
    load_dotenv(dotenv_path=dotenv_path)


@click.command()
@click.option('-d', '--directory', type=click.Path(exists=True))
def email(directory: Path):
    try:
        load_gmail_environment_variables()
    except ConfigurationError as e:
        message = f'Could not load email environment variables. Error {e}'
        click.secho(message, fg='red')
        sys.exit(100)

    files_to_email: List[Dict[str, Any]] = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            short_name, invoice_number = get_invoice_info_from_filename(file)
            if invoice_number != 0:
                invoice_dict = {'file': Path(root) / file,
                                'short_name': short_name,
                                'invoice_number': invoice_number}
                files_to_email.append(invoice_dict)
                # click.secho(f'{file}', fg='blue')
    files_to_email = sorted(files_to_email, key=lambda x: x['file'].name)

    for idx, r_file in enumerate(files_to_email, 1):
        click.secho(f'{idx} {r_file["file"].parent}/{r_file["file"].name}', fg='yellow')
    file_num = click.prompt('Select file to rename', type=int)
    file_data_to_email = files_to_email[file_num - 1]
    # print(Path(file_to_email))
    invoice_file: Path = file_data_to_email['file']
    # webbrowser.open_new_tab(str(invoice_file.absolute()))
    recipient = os.getenv('CMMI_EMAIL')
    print(f'{recipient}')
    try:
        sender = SenderConfig(password=os.getenv('GMAIL_SECRET'),
                              email=os.getenv('GMAIL_USER'))
        print(sender)
    except ValidationError:
        message = 'Cannot build configuration. Either the GMAIL_SECRET or GMAIL_USER enviroment variables are not set.'
        click.secho(message, fg='red')
        sys.exit(100)

    invoice_number = int(invoice_file.name.split('-')[2])
    invoice_number = click.prompt('Invoice number', default=invoice_number)
    month = click.prompt('Month, ie. agosto')
    year = click.prompt('Year', default=2023)
    service_type = click.prompt('Service type', default='mantenimiento')
    service = f'{service_type} de {month} {year}'  # fixme
    amount = '220.00'  # fixme
    amount = click.prompt('Amount', default=amount)
    template_folder = Path(__file__).parent.parent / 'templates'
    content_file = template_folder / 'tailwind_invoice_template_email.html'
    with open(content_file, 'r') as f:
        content_template = f.read()

    subject = f'Factura Fiscal No. {invoice_number} por {service}'
    content = content_template.format(
        invoice_number=invoice_number,
        service=service, amount=amount
    )
    pprint(content)
    email_message = EmailMessage(
        sender_config=sender,
        recipients=[recipient],
        attachments=[invoice_file],
        subject=subject,
        content=content,
        format=EmailFormat.HTML
    )

    # raise Exception('xxx')  # FIXME
    c = click.confirm('Send')
    if c:
        response = send_email(email_message)
        print(response)
    else:
        print('not sent')
