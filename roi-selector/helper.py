import cv2


def put_text_with_background(
    image, instructions, cv_font=cv2.FONT_HERSHEY_PLAIN, position="top-right"
):
    if image is None:
        raise ValueError("Input image is None.")

    font = cv_font
    image_with_instructions = image.copy()
    height, width, _ = image_with_instructions.shape

    text_size = cv2.getTextSize(max(instructions, key=len), font, 1, 2)[0]
    padding = 10
    bg_height = len(instructions) * text_size[1] + padding * 2
    bg_width = text_size[0] + padding * 3

    position_mapping = {
        "top-left": (0, 0),
        "top-right": (width - bg_width, 0),
        "bottom-left": (0, height - bg_height),
        "bottom-right": (width - bg_width, height - bg_height),
        "center": ((width - bg_width) // 2, (height - bg_height) // 2),
    }

    if position not in position_mapping:
        raise ValueError(
            "Invalid position. Supported positions: 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'"
        )

    start_point = position_mapping[position]

    cv2.rectangle(
        image_with_instructions,
        start_point,
        (start_point[0] + bg_width, start_point[1] + bg_height),
        (0, 0, 255),
        -1,
    )

    for idx, instruction in enumerate(instructions):
        y = start_point[1] + (idx + 1) * text_size[1] + padding
        cv2.putText(
            image_with_instructions,
            instruction,
            (start_point[0] + padding, y),
            font,
            1,
            (255, 255, 255),
            1,
        )

    return image_with_instructions
