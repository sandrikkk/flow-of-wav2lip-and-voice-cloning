"""Module to handle text translation using Google Cloud Translate."""

import logging

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import translate_v2 as translate


def translate_text(target: str, text: str | bytes) -> str:

    """
    Translate text into the specified target language using Google Cloud Translate.

    Arguments:
        target -- The ISO 639-1 language code to which the text will be translated.
        text -- The text or bytes to translate.

    Raises:
        TypeError: If 'text' is neither a string nor bytes.
        GoogleAPICallError: If the Google API call fails.
        ClientError: If the client encounters an error during execution.

    Returns:
        A dictionary containing the input text, the translated text, and the detected
        source language.

    """

    logging.basicConfig(level=logging.INFO)
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")
    elif not isinstance(text, str):
        raise TypeError("Text must be an instance of str or bytes.")

    try:
        result = translate_client.translate(text, target_language=target)
    except GoogleAPICallError as api_error:
        logging.error("Google API call failed: %s", api_error)
        raise

    logging.info("Text: %s", result["input"])
    logging.info("Translation: %s", result["translatedText"])
    logging.info("Detected source language: %s", result["detectedSourceLanguage"])

    translated_text: str = result["translatedText"]

    return translated_text


if __name__ == "__main__":
    text = '''
    vamos a ver cómo colocar correctamente todos los accesorios de mambo cooking os recuerdo que mambo cooking total gourmet dispone de dos jarras Victory y unic cada una con sus accesorios específicos los accesorios específicos para la jarra Victory llevan serigrafía una V para que no confundáis en qué jarra colocarlos y los accesorios de la jarra unit llevan serigrafiada una U de unic dentro de la jarra encontramos el engranaje que es común para ambas jarras si en alguna ocasión queremos retirarlo simplemente tenemos que girar el accesorio que lo sujeta y extraerlo por la parte superior la mayoría de accesorios tanto de la jarra Víctor y como de la jarra unique son one click debemos introducirlos sobre el engranaje presionar un poquito hacia abajo y girar a la izquierda para que queden totalmente anclados para extraerlos volvemos a presionar un poquito hacia abajo y giramos a la derecha dependiendo del accesorio que elijamos en el robot estaremos limitados por velocidades por ejemplo si  las cuchillas de Victory o unit tendremos disponibles todos los rangos de velocidades si elegimos las cucharas mambo mix la velocidad máxima será de 3 la mariposa debe colocarse siempre con las cuchillas puestas presionando sobre el tornillo las varillas double wish os llegan desmontadas en el embalaje simplemente tenéis que presionar y lo colocamos directamente también sobre el engranaje para poder montar claras a punto de nieve o hacer nada y el innovador accesorio sote Blade con el que podrás hacer diferentes tipos de recetas la tapa se coloca directamente sobre el vocal de la jarra giramos y ya queda firmemente sellada el vaso medidor lo colocamos y lo giramos para que también quede cerrado el cestillo nos servirá para cocinar al vapor o hacer una segunda elaboración mientras estamos cocinando otra debajo y simplemente debemos introducirlo en la jarra con la espátula podrás remover manualmente cualquier elaboración y te ayudará a la hora de  con la vaporera podremos cocinar de dos maneras si estamos con velocidad cero podremos cocinar directamente sobre la jarra si estamos haciendo alguna elaboración que precisa movimiento bien de cuchillas bien de mambo mix entonces tendremos que tener la tapa colocada vaso medidor retirado y colocar la vaporera sobre el lado el procesador de ingredientes la jarra unic se coloca de la siguiente manera tenéis dos orificios en el disco para que no os cortéis introducir esta pieza sobre el engranaje y el disco por la parte que necesitéis bien para rallar o bien para laminar a continuación colocamos la tapa específica del procesador el ingrediente y nos ayudamos del empujador para rallar o laminar el accesorio limpiador tiene dos posiciones una más estrecha para la jarra Victory y otra más ancha para la jarra Unix y ahora vamos con el innovador dispensador de ingredientes chef Crown cuando estéis cocinando con él simplemente lo  ponéis sobre ella y gira para que quede cerrado a continuación se os pedirá que tais chef Crown para que mambo pueda comenzar a cocinar vamos a ver por último las partes que componen chef su capa en la que encontráis una rejilla que se puede sacar para una mejor limpieza girando la pestaña tenemos el plato de aluminio  a continuación un aro de silicona que nos da la estanqueidad en la corona  compuesto de dos partes una con orificios que es la que siempre quedará en la parte exterior y otra asignada que es la que queda en la parte interior de la corona y la corona en sí con seis compartimientos y por último tenemos el cuerpo principal del chef que se compone de las siguientes partes esta etapa inferior que podemos extraer para su mejor limpieza y el
    '''
    translated = translate_text("en", text)
    print(translated)
