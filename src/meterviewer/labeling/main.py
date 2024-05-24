from turtle import onkey
from nicegui import ui
from nicegui.events import ValueChangeEventArguments, KeyEventArguments
from meterviewer import files
from meterviewer.datasets import dataset
from meterviewer.labeling.config import get_root_path


def show(event: ValueChangeEventArguments):
    name = type(event.sender).__name__
    ui.notify(f"{name}: {event.value}")


def old_layout():
    ui.button("Button", on_click=lambda: ui.notify("Click"))
    with ui.row():
        ui.checkbox("Checkbox", on_change=show)
        ui.switch("Switch", on_change=show)
    ui.radio(["A", "B", "C"], value="A", on_change=show).props("inline")
    with ui.row():
        ui.input("Text input", on_change=show)
        ui.select(["One", "Two"], value="One", on_change=show)


def main():
    ui.markdown("# Labeling tool for meter image.")

    root_path = get_root_path()

    def handle_key(e: KeyEventArguments):
        if e.key == "Enter":
            if e.action.keyup:
                set_img_value()

    _ = ui.keyboard(handle_key)

    def get_image_path():
        for dataset_name in dataset.get_dataset_list(root_path):
            img_p = files.scan_pics(dataset.get_dataset_path(root_path, str(dataset_name)))
            yield img_p, dataset_name

    dataset_g = get_image_path()
    img_path_g, dataset_name = next(dataset_g)

    image_name = str(next(img_path_g))
    carry_v = None

    def set_img_value():
        nonlocal carry_v
        if carry_v is None:
            return
        print(f"image_name: {image_name}")
        print(f"value_set: {carry_v}")
        current_img.source = next(img_path_g)
        toggle1.set_value(None)

    def set_value(event: ValueChangeEventArguments):
        nonlocal carry_v
        carry_v = event.value
        set_img_value()

    ui.markdown(f"dataset: {dataset_name}, count: 1/20222")
    with ui.row():
        current_img = ui.image(image_name).classes("w-[540px]")

    with ui.row():
        toggle1 = ui.toggle([0, 1, 2, 3, 4, 5, 6], value=carry_v, on_change=set_value)
        ui.input("Carry digit", on_change=set_value)
    with ui.row():
        ui.button("previous")
        ui.button("confirm", on_click=lambda: set_img_value())
    # ui.link("And many more...", "/documentation").classes("mt-8")

    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
