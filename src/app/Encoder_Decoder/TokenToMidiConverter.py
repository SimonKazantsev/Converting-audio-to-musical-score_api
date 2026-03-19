import pretty_midi


class TokenToMidiConverter:
    """Конвертация токенов модели в MIDI."""

    def __init__(self, output_path: str):
        """Инициализация."""
        self.output_path = output_path

    def convert(self, events):
        """Конвертирует список событий токенизатора в MIDI-файл."""
        pm = pretty_midi.PrettyMIDI()
        inst = pretty_midi.Instrument(program=0)

        # Активные ноты: pitch → (start_time, velocity)
        active: dict[int, tuple[float, int]] = {}
        current_velocity = 64

        for (time_sec, etype, pitch, velocity) in events:
            if etype == "NOTE_ON":
                active[pitch] = (time_sec, velocity)
            elif etype == "NOTE_OFF":
                if pitch in active:
                    start, vel = active.pop(pitch)
                    end = max(start + 0.05, time_sec)   # минимальная длительность
                    note = pretty_midi.Note(
                        velocity=vel, pitch=pitch,
                        start=start, end=end
                    )
                    inst.notes.append(note)
            max_time = max((n.end for n in inst.notes), default=0.0)
        for pitch, (start, vel) in active.items():
            inst.notes.append(pretty_midi.Note(
                velocity=vel, pitch=pitch,
                start=start, end=max_time + 0.1
            ))

        pm.instruments.append(inst)
        pm.write(self.output_path)
        print(f"MIDI сохранён: {self.output_path}  ({len(inst.notes)} нот)")