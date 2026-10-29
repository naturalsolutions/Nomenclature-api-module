"""English labels and definitions of the SINP nomenclatures

Revision ID: 626c1cdaafeb
Revises:
Create Date: 2026-10-29 18:30:00

Optional branch, translations made by Natural Solutions (no official English version
of the SINP nomenclatures). Only empty values are filled. The downgrade sets back to
NULL the values still equal to the ones set here, a value typed by hand with the same
text included.
"""

import csv
import importlib.resources

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "626c1cdaafeb"
down_revision = None
branch_labels = ("nomenclatures_inpn_data_en",)
depends_on = ("8eb9a12db289",)  # last revision of nomenclatures_inpn_data


def read_csv(name):
    content = importlib.resources.read_text("pypnnomenclature.migrations.data", name)
    return list(csv.DictReader(content.splitlines()))


def upgrade():
    conn = op.get_bind()
    for column in ("label_en", "definition_en"):
        conn.execute(
            text(f"""
                UPDATE ref_nomenclatures.t_nomenclatures n SET {column} = :value
                FROM ref_nomenclatures.bib_nomenclatures_types t
                WHERE n.id_type = t.id_type AND t.mnemonique = :type
                  AND n.cd_nomenclature = :cd_nomenclature AND coalesce(n.{column}, '') = ''
            """),
            [
                {**row, "value": row[column]}
                for row in read_csv("nomenclatures_inpn_data_en.csv")
                if row[column]
            ],
        )
        conn.execute(
            text(f"""
                UPDATE ref_nomenclatures.bib_nomenclatures_types SET {column} = :value
                WHERE mnemonique = :type AND coalesce({column}, '') = ''
            """),
            [
                {**row, "value": row[column]}
                for row in read_csv("nomenclatures_types_en.csv")
                if row[column]
            ],
        )


def downgrade():
    conn = op.get_bind()
    for column in ("label_en", "definition_en"):
        conn.execute(
            text(f"""
                UPDATE ref_nomenclatures.t_nomenclatures n SET {column} = NULL
                FROM ref_nomenclatures.bib_nomenclatures_types t
                WHERE n.id_type = t.id_type AND t.mnemonique = :type
                  AND n.cd_nomenclature = :cd_nomenclature AND n.{column} = :value
            """),
            [
                {**row, "value": row[column]}
                for row in read_csv("nomenclatures_inpn_data_en.csv")
                if row[column]
            ],
        )
        conn.execute(
            text(f"""
                UPDATE ref_nomenclatures.bib_nomenclatures_types SET {column} = NULL
                WHERE mnemonique = :type AND {column} = :value
            """),
            [
                {**row, "value": row[column]}
                for row in read_csv("nomenclatures_types_en.csv")
                if row[column]
            ],
        )
