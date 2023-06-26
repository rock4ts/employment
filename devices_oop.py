

class SpeakerDevice:
    """
    Родительский класс для устройств с функцией управления звуком.

    Атрибуты экземпляров:
        power - значение включён/выключен
        min_volume - минимальное значение громкости звука
        max_volume - максимальное значение громкости звука
        volume - текущая громкость звука

    Методы:
        turn_on - функция включения устройства
        turn_off - функция выключения устройства
        set_volume - функция настройки уровня звука
    """

    def __init__(
            self,
            model: str,
            power: bool = False,
            min_volume: int = 0,
            max_volume: int = 10,
            volume: float = 5):
        self.model = model
        self.power = power
        self.volume = round(volume * 2) / 2
        self.min_volume = min_volume
        self.max_volume = max_volume

    def turn_on(self) -> None:
        """Функция включения устройства."""
        if self.power == False:
            self.power = True
            print("Устройство включено")
        else:
            print("Устройство уже включено")

    def turn_off(self) -> None:
        """Функция выключения устройства."""
        if self.power == True:
            self.power = False
            print("Устройство выключено")
        else:
            print("Устройство уже выключено")

    def set_volume(self, volume: float) -> None:
        """
        Функция настройки уровня звука.
        
        :volume - значение устанавливаемого уровеня звука
        """
        if self.power == False:
            print(
                "Функция регулирования уровня громкости "
                "для выключенного девайса недоступна.")
        elif 0 <= volume <= 10:
            self.volume = round(volume * 2) / 2
            print(f"Уровень громкости установлен на {self.volume}")

        else:
            print(
                "Громкость звука должна задаваться "
                "действительным неотрицательным числом "
                f"в пределах от {self.min_volume} до {self.max_volume}.")


class Radio(SpeakerDevice):
    """
    Класс-родитель для всех радио устройств, наследник класса SpeakerDevice.

    Атрибуты экземпляров:
        min_frequency - нижний предел радио частоты
        max_frequency - верхний предел радио частоты
        radiofrequency - текущая радио частота устройства
    Методы:
        set_frequency - устанавливает запрашиваемую волну

    
    """

    def __init__(self,
                 model: str,
                 min_volume: int = 0,
                 max_volume: int = 10,
                 power: bool = False,
                 volume: float = 5,
                 min_frequency: float = 87.5,
                 max_frequency: float = 108.0,
                 radiofrequency: float = 87.5):
        super().__init__(model, power, volume, min_volume, max_volume)
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.radiofrequency = round(radiofrequency, 1)

    def set_frequency(self, new_frequency: float) -> None:
        """
        Устанавливает запрашиваемую волну.

        :new_frequency - запрашиваемая волна
        """
        frequency_allowed = (
            self.min_frequency <= new_frequency <= self.max_frequency)
        if self.power and frequency_allowed:
            self.radiofrequency = round(new_frequency, 1)
            print(f"Установлена радиочастота {self.radiofrequency}")
        elif not self.power:
            print("Включите устройство.")
        else:
            print("Радиочастота должна задаваться неотрицательным числом "
                  f"в пределах {self.min_frequency} и {self.max_frequency}")


class TV(SpeakerDevice):
    """
    Класс-родитель для всех типов телевизоров, наследник класса SpeakerDevice.

    Методы:
        switch_input_source - меняет источник входного сигнала
        switch_channel - меняет просматриваемый канал
    
    Класс можно расширить
    и добавить другие, общие для всех телевизоров методы управления,
    а также создать классы-наследники,
    конкретизирующие атрибуты и методы
    конкретной категории и модели телевизора,
    например для ЖК-телевизора с функцией "SMART TV".
    """

    def __init__(
            self,
            model: str,
            display_size: float,
            min_volume: int = 0,
            max_volume: int = 10,
            power: bool = False,
            volume: float = 5,
            input_sources: list = ["HDMI", "AV", "SCART"],
            start_channel: int = 1,
            max_channels: int = 100):
        super().__init__(model, power, volume, min_volume, max_volume)
        self.display_size = display_size
        self.input_sources = input_sources
        self.input_source = input_sources[0]
        self.start_channel = start_channel
        self.max_channels = max_channels
        self.channel = start_channel

    def switch_input_source(self, new_input_source: str) -> None:
        """
        Меняет источник входного сигнала, если он есть в списке доступных.

        :new_input_source - новый источник входного сигнала
        """
        input_source_exists = new_input_source in self.input_sources
        is_diff = new_input_source != self.input_source
        if self.power and input_source_exists and is_diff:
            self.input_source = new_input_source
            print(
                "В качестве источника входного сигнала "
                f"установлен на {self.input_source}")
        elif not self.power:
            print("Включите устройство.")
        else:
            input_sources_str = (
                ', '.join(input_source for input_source in self.input_sources)
            )
            print(
                f"Источника входного сигнала {new_input_source} "
                f"нет в списке доступных: {input_sources_str}")

    def switch_channel(self, new_channel: int) -> None:
        """
        Меняет телевизионный канал, если он существует.

        :new_channel - новый телевизионный канал
        """
        channel_exists = (
            isinstance(new_channel, int)
            and self.start_channel < new_channel < self.max_channels
        )
        is_different = new_channel != self.channel

        if self.power and channel_exists and is_different:
            self.channel = new_channel
            print(f"Включён {self.channel} канал.")
        elif not self.power:
            print("Включите устройство.")
        elif new_channel == self.channel:
            print("Указанный канал уже включён.")
        else:
            print(
                "Номер канала задаётся "
                "целым неотрицательным числом в диапазоне "
                f"от {self.start_channel} до {self.max_channels}.")


class MobilePhone(SpeakerDevice):
    """
    Класс-родитель для всех типов мобильных телефонов,
    наследник класса SpeakerDevice.

    Методы:
        make_call - функция исходящего звонка
        receive_call - функция входящего звонка
        send_message - функция отправки сообщения
        receive_message - функция получения сообщения

    Класс можно расширить
    и добавить другие, общие для всех мобильных телефонов методы управления,
    а также создать классы-наследники,
    конкретизирующие атрибуты и функции модели и ПО,
    например для телефонов SAMSUNG работающих на базе Android.
    """

    def __init__(
            self,
            model: str,
            display_size: float,
            has_camera: bool = True,
            power: bool =False,
            min_volume: int = 0,
            max_volume: int = 10,
            volume: int = 5):
        super().__init__(model, power, min_volume, max_volume, volume)
        self.display_size = display_size
        self.has_camera = has_camera

    def make_call(self, name: str, number: str) -> None:
        """
        Функция исходящего звонка.

        :name - имя адрессата звонка
        :number - номер адрессата звонка
        """
        if self.power:
            print(f"Звоним: {name} ({number})")
        else:
            print("Включите устройство")

    def receive_call(self, name: str, number: str) -> None:
        """
        Функция входящего звонка.

        :name - имя звонящего
        :number - номер звонящего
        """
        if self.power:
            print(f"Вам звонит {name} ({number}), ответить на звонок?")
            answer = True if input() == "Да" else False
        else:
            return

        if answer:
            print(f"Привет, {name}!")
        else:
            text = "Я не могу сейчас разговаривать, перезвоню позже."
            self.send_message(name, number, text)

    def send_message(self, name: str, number: str, text: str) -> None:
        """
        Функция отправки сообщения.

        :name - имя адрессата сообщения
        :number - номер адрессата сообщения
        :text - текст отправленного сообщения
        """
        if self.power:
            print(f"{name} ({number}) отправлено сообщение: \"{text}\"")
        else:
            print("Включите устройство.")

    def receive_message(self, name: str, number: str, text: str) -> None:
        """Функция получения сообщения.
        
        :name - имя адрессанта сообщения
        :number - номер адрессанта сообщения
        :text - текст полученного сообщения
        """
        if self.power:
            print(f"{name} ({number}) прислал(а) сообщение: \"{text}\"")


new_tv = TV('Some classy TV', 40)
print(new_tv.model)
print(new_tv.display_size)
new_tv.switch_input_source('AV')
print(new_tv.input_source)
new_tv.switch_channel(2)
print(new_tv.channel)

new_tv.turn_on()
new_tv.switch_input_source('AV')
print(new_tv.input_source)
new_tv.switch_channel(2)
print(new_tv.channel)