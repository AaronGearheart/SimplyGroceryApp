import flet as ft
import getLocations
import GSAPI

def main(page: ft.Page):

    def get_locations_click(e):
        postal_code = 76226
        locations = getLocations.get_locations(postal_code) 
        
        column.controls.clear()

        for lid, name in locations.items():
            location_button = ft.ElevatedButton(
                text=name,
                on_click=lambda lid=lid: update_output_with_lid(lid)
            )
            location_button.data = lid
            column.controls.append(location_button)

        # Re-add other controls (in this case, "Update List" and output)
        column.controls.append(get_locations_button)
        column.controls.append(update_list_button)
        column.controls.append(output)

        page.update()
        
    def update_list_click(e):
        selected_lid = page.client_storage.get("lid")
        response = GSAPI.update_list("53990804-cfd1-43f3-8256-bdc9817a4fd0", selected_lid, "ais")
        print(response)

    def update_output_with_lid(e):
        lid = e.control.data
        page.client_storage.set("lid", lid)
        output.value = f"LID: {lid}"
        page.update()

    page.title = "Simply Grocery"

    get_locations_button = ft.ElevatedButton(text="Get Locations", on_click=get_locations_click)
    update_list_button = ft.ElevatedButton(text="Update List", on_click=update_list_click)
    output = ft.Text(
        "",
        size=10,
    )

    column = ft.Column(
        controls=[
            get_locations_button,
            update_list_button,
            output
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    container = ft.Container(
        content=column,
        alignment=ft.alignment.center,
        padding=20,
        border=ft.border.all(1, ft.colors.BLACK12),
    )

    row = ft.Row(
        controls=[container],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    page.add(row)
    page.update()

ft.app(target=main)
