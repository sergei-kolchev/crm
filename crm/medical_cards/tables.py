from tables import schemas, fields, buttons
from tables.html import HTMLAttributes


class MedicalCardsTable(schemas.TableSchema):
    number = fields.TextField(
        verbose_name="№",
        #view_name_th="medical_cards:cards",
        attrs_th=HTMLAttributes(attrs={"style": "width: 10%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )
    hospitalization = fields.TextField(
        verbose_name="Госпитализация",
        #view_name_th="medical_cards:cards",
        attrs_th=HTMLAttributes(attrs={"style": "width: 30%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )
    diagnosis = fields.TextField(
        verbose_name="Диагноз",
        attrs_th=HTMLAttributes(attrs={"style": "width: 30%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )
    actions = fields.ButtonsField(
        verbose_name="Действия",
        buttons=[
            buttons.UpdateInlineButton(
                name="Изменить", view_name="medical_cards:update"
            ),
            buttons.DeleteButton(
                name="Удалить", view_name="medical_cards:delete"
            ),
        ],
        attrs_th=HTMLAttributes(attrs={"style": "width: 30%"}),
        attrs_td=HTMLAttributes(attrs={"class": "align-middle text-center"}),
    )

    class Meta:
        index = ("number", "diagnosis", "hospitalization", "actions")