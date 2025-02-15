"""Autogenerated module for the SHFSG QCoDeS driver."""
from typing import Any, Dict, List, Tuple, Union
from zhinst.toolkit import CommandTable, Waveforms, Sequence
from zhinst.qcodes.driver.devices.base import ZIBaseInstrument
from zhinst.qcodes.qcodes_adaptions import ZINode, ZIChannelList


class CommandTableNode(ZINode):
    """CommandTable node.

    This class implements the basic functionality of the command table allowing
    the user to load and upload their own command table.

    A dedicated class called ``CommandTable`` exists that is the preferred way
    to create a valid command table. For more information about the
    ``CommandTable`` refer to the corresponding example or the documentation
    of that class directly.

    Args:
        root: Node used for the upload of the command table
        tree: Tree (node path as tuple) of the current node
        device_type: Device type.
    """

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, "commandtable", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object

    def check_status(self) -> bool:
        """Check status of the command table.

        Returns:
            Flag if a valid command table is loaded into the device.

        Raises:
            RuntimeError: If the command table upload into the device failed.
        """
        return self._tk_object.check_status()

    def load_validation_schema(self) -> Dict[str, Any]:
        """Load device command table validation schema.

        Returns:
            JSON validation schema for the device command tables.
        """
        return self._tk_object.load_validation_schema()

    def upload_to_device(
        self,
        ct: Union[CommandTable, str, dict],
        *,
        validate: bool = False,
        check_upload: bool = True,
    ) -> None:
        """Upload command table into the device.

        The command table can either be specified through the dedicated
        ``CommandTable`` class or in a raw format, meaning a json string or json
        dict. In the case of a json string or dict the command table is
        validated by default against the schema provided by the device.

        Args:
            ct: Command table.
            validate: Flag if the command table should be validated. (Only
                applies if the command table is passed as a raw json string or
                json dict)
            check_upload: Flag if the upload should be validated by calling
                `check_status`. This is not mandatory bat strongly recommended
                since the device does not raise an error when it rejects the
                command table. This Flag is ignored when called from within a
                transaction.

        Raises:
            RuntimeError: If the command table upload into the device failed.
            zhinst.toolkit.exceptions.ValidationError: Incorrect schema.

        .. versionchanged:: 0.4.2

            New Flag `check_upload` that makes the upload check optional.
            `check_status` is only called when not in a ongoing transaction.
        """
        return self._tk_object.upload_to_device(
            ct=ct, validate=validate, check_upload=check_upload
        )

    def load_from_device(self) -> CommandTable:
        """Load command table from the device.

        Returns:
            command table.
        """
        return self._tk_object.load_from_device()


class AWGCore(ZINode):
    """AWG Core Node."""

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, "awg", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object
        if self._tk_object.commandtable:

            self.add_submodule(
                "commandtable",
                CommandTableNode(
                    self,
                    self._tk_object.commandtable,
                    zi_node=self._tk_object.commandtable.node_info.path,
                    snapshot_cache=self._snapshot_cache,
                ),
            )

    def enable_sequencer(self, *, single: bool) -> None:
        """Starts the sequencer of a specific channel.

        Warning:
            This function is synchronous and blocks until the sequencer is enabled.
            When working with multiple instruments this function is the wrong
            approach and the sequencer should be enabled asynchronously.
            (For more information please take a look at the awg example in the
            toolkit documentation.)

        Args:
            single: Flag if the sequencer should be disabled after finishing
            execution.

        Raises:
            RuntimeError: If the sequencer could not be enabled.

        .. versionchanged:: 0.4.4

            Check the acknowledged value instead of using `wait_for_state_change`.
        """
        return self._tk_object.enable_sequencer(single=single)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.005) -> None:
        """Wait until the AWG is finished.

        Args:
            timeout: The maximum waiting time in seconds for the generator
                (default: 10).
            sleep_time: Time in seconds to wait between requesting generator
                state

        Raises:
            RuntimeError: If continuous mode is enabled
            TimeoutError: If the sequencer program did not finish within
                the specified timeout time
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def compile_sequencer_program(
        self, sequencer_program: Union[str, Sequence], **kwargs: Union[str, int]
    ) -> Tuple[bytes, Dict[str, Any]]:
        """Compiles a sequencer program for the specific device.

        Args:
            sequencer_program: The sequencer program to compile.

        Keyword Args:
            samplerate: Target sample rate of the sequencer. Only allowed/
                necessary for HDAWG devices. Must correspond to the samplerate
                used by the device (device.system.clocks.sampleclock.freq()).
                If not specified the function will get the value itself from
                the device. It is recommended passing the samplerate if more
                than one sequencer code is uploaded in a row to speed up the
                execution time.
            wavepath: path to directory with waveforms. Defaults to path used
                by LabOne UI or AWG Module.
            waveforms: waveform CSV files separated by ';'
            output: name of embedded ELF filename.

        Returns:
            elf: Binary ELF data for sequencer.
            extra: Extra dictionary with compiler output.

        Examples:
            >>> elf, compile_info = device.awgs[0].compile_sequencer_program(seqc)
            >>> device.awgs[0].elf.data(elf)
            >>> device.awgs[0].ready.wait_for_state_change(1)
            >>> device.awgs[0].enable(True)

        Raises:
            RuntimeError: `sequencer_program` is empty.
            RuntimeError: If the compilation failed.

        .. versionadded:: 0.4.0
        """
        return self._tk_object.compile_sequencer_program(
            sequencer_program=sequencer_program, **kwargs
        )

    def load_sequencer_program(
        self, sequencer_program: Union[str, Sequence], **kwargs: Union[str, int]
    ) -> Dict[str, Any]:
        """Compiles the given sequencer program on the AWG Core.

        Warning:
            After uploading the sequencer program one needs to wait before for
            the awg core to become ready before it can be enabled.
            The awg core indicates the ready state through its `ready` node.
            (device.awgs[0].ready() == True)

        Args:
            sequencer_program: Sequencer program to be uploaded.

        Keyword Args:
            samplerate: Target sample rate of the sequencer. Only allowed/
                necessary for HDAWG devices. Must correspond to the samplerate
                used by the device (device.system.clocks.sampleclock.freq()).
                If not specified the function will get the value itself from
                the device. It is recommended passing the samplerate if more
                than one sequencer code is uploaded in a row to speed up the
                execution time.
            wavepath: path to directory with waveforms. Defaults to path used
                by LabOne UI or AWG Module.
            waveforms: waveform CSV files separated by ';'
            output: name of embedded ELF filename.

        Examples:
            >>> compile_info = device.awgs[0].load_sequencer_program(seqc)
            >>> device.awgs[0].ready.wait_for_state_change(1)
            >>> device.awgs[0].enable(True)

        Raises:
            RuntimeError: `sequencer_program` is empty.
            RuntimeError: If the upload or compilation failed.

        .. versionadded:: 0.3.4

            `sequencer_program` does not accept empty strings

        .. versionadded:: 0.4.0

            Use offline compiler instead of AWG module to compile the sequencer
            program. This speeds of the compilation and also enables parallel
            compilation/upload.
        """
        return self._tk_object.load_sequencer_program(
            sequencer_program=sequencer_program, **kwargs
        )

    def write_to_waveform_memory(
        self, waveforms: Waveforms, indexes: list = None
    ) -> None:
        """Writes waveforms to the waveform memory.

        The waveforms must already be assigned in the sequencer program.

        Args:
            waveforms: Waveforms that should be uploaded.
            indexes: Specify a list of indexes that should be uploaded. If
                nothing is specified all available indexes in waveforms will
                be uploaded. (default = None)

        .. versionchanged:: 0.4.2

            Removed `validate` flag and functionality. The validation check is
            now done in the `Waveforms.validate` function.
        """
        return self._tk_object.write_to_waveform_memory(
            waveforms=waveforms, indexes=indexes
        )

    def read_from_waveform_memory(self, indexes: List[int] = None) -> Waveforms:
        """Read waveforms from the waveform memory.

        Args:
            indexes: List of waveform indexes to read from the device. If not
                specified all assigned waveforms will be downloaded.

        Returns:
            Waveform object with the downloaded waveforms.
        """
        return self._tk_object.read_from_waveform_memory(indexes=indexes)

    def configure_marker_and_trigger(
        self, *, trigger_in_source: str, trigger_in_slope: str, marker_out_source: str
    ) -> None:
        """Configures the trigger inputs and marker outputs of the AWG.

        Args:
            trigger_in_source: Alias for the trigger input used by the
                sequencer. For a list of available values use:
                `available_trigger_inputs`
            trigger_in_slope: Alias for the slope of the input trigger
                used by sequencer. For a list of available values use
                `available_trigger_inputs`
            marker_out_source: Alias for the marker output source used by
                the sequencer. For a list of available values use
                `available_trigger_slopes`
        """
        return self._tk_object.configure_marker_and_trigger(
            trigger_in_source=trigger_in_source,
            trigger_in_slope=trigger_in_slope,
            marker_out_source=marker_out_source,
        )

    @property
    def available_trigger_inputs(self) -> List:
        """List the available trigger sources for the sequencer."""
        return self._tk_object.available_trigger_inputs

    @property
    def available_trigger_slopes(self) -> List:
        """List the available trigger slopes for the sequencer."""
        return self._tk_object.available_trigger_slopes

    @property
    def available_marker_outputs(self) -> List:
        """List the available trigger marker outputs for the sequencer."""
        return self._tk_object.available_marker_outputs


class SGChannel(ZINode):
    """Signal Generator Channel for the SHFSG.

    :class:`SGChannel` implements basic functionality to configure SGChannel
    settings of the :class:`SHFSG` instrument.

    Args:
        device: SHFQA device object.
        session: Underlying session.
        tree: Node tree (node path as tuple) of the corresponding node.
    """

    def __init__(self, parent, tk_object, index, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"sgchannel_{index}",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object
        if self._tk_object.awg:

            self.add_submodule(
                "awg",
                AWGCore(
                    self,
                    self._tk_object.awg,
                    zi_node=self._tk_object.awg.node_info.path,
                    snapshot_cache=self._snapshot_cache,
                ),
            )

    def configure_channel(
        self, *, enable: bool, output_range: int, center_frequency: float, rf_path: bool
    ) -> None:
        """Configures the RF input and output.

        Args:
            enable: Flag if the signal output should be enabled.
            output_range: Maximal range of the signal output power in dBm
            center_frequency: Center frequency before modulation
            rf_path: Flag if the RF(True) or LF(False) path should be
                configured.
        """
        return self._tk_object.configure_channel(
            enable=enable,
            output_range=output_range,
            center_frequency=center_frequency,
            rf_path=rf_path,
        )

    def configure_pulse_modulation(
        self,
        *,
        enable: bool,
        osc_index: int = 0,
        osc_frequency: float = 100000000.0,
        phase: float = 0.0,
        global_amp: float = 0.5,
        gains: tuple = (1.0, -1.0, 1.0, 1.0),
        sine_generator_index: int = 0,
    ) -> None:
        """Configure the pulse modulation.

        Configures the sine generator to digitally modulate the AWG output, for
        generating single sideband AWG signals

        Args:
            enable: Flag if the modulation should be enabled.
            osc_index: Selects which oscillator to use
            osc_frequency: Oscillator frequency used to modulate the AWG
                outputs. (default = 100e6)
            phase: Sets the oscillator phase. (default = 0.0)
            global_amp: Global scale factor for the AWG outputs. (default = 0.5)
            gains: Sets the four amplitudes used for single sideband generation.
                Default values correspond to upper sideband with a positive
                oscillator frequency. (default = (1.0, -1.0, 1.0, 1.0))
            sine_generator_index: Selects which sine generator to use on a
                given channel.
        """
        return self._tk_object.configure_pulse_modulation(
            enable=enable,
            osc_index=osc_index,
            osc_frequency=osc_frequency,
            phase=phase,
            global_amp=global_amp,
            gains=gains,
            sine_generator_index=sine_generator_index,
        )

    def configure_sine_generation(
        self,
        *,
        enable: bool,
        osc_index: int = 0,
        osc_frequency: float = 100000000.0,
        phase: float = 0.0,
        gains: tuple = (0.0, 1.0, 1.0, 0.0),
        sine_generator_index: int = 0,
    ) -> None:
        """Configures the sine generator output.

        Configures the sine generator output of a specified channel for generating
        continuous wave signals without the AWG.

        Args:
            enable: Flag if the sine generator output should be enabled.
            osc_index: Selects which oscillator to use
            osc_frequency: Oscillator frequency used by the sine generator
                (default = 100e6)
            phase: Sets the oscillator phase. (default = 0.0)
            gains: Sets the four amplitudes used for single sideband
                generation. Default values correspond to upper sideband with a
                positive oscillator frequency.
                Gains are set in the following order I/sin, I/cos, Q/sin, Q/cos.
                (default = (0.0, 1.0, 1.0, 0.0))
            sine_generator_index: Selects which sine generator to use on a given
                channel
        """
        return self._tk_object.configure_sine_generation(
            enable=enable,
            osc_index=osc_index,
            osc_frequency=osc_frequency,
            phase=phase,
            gains=gains,
            sine_generator_index=sine_generator_index,
        )

    @property
    def awg_modulation_freq(self) -> float:
        """Modulation frequency of the AWG.

        Depends on the selected oscillator.
        """
        return self._tk_object.awg_modulation_freq


class SHFSG(ZIBaseInstrument):
    """QCoDeS driver for the Zurich Instruments SHFSG."""

    def _init_additional_nodes(self):
        """Init class specific modules and parameters."""
        if self._tk_object.sgchannels:

            channel_list = ZIChannelList(
                self,
                "sgchannels",
                SGChannel,
                zi_node=self._tk_object.sgchannels.node_info.path,
                snapshot_cache=self._snapshot_cache,
            )
            for i, x in enumerate(self._tk_object.sgchannels):
                channel_list.append(
                    SGChannel(
                        self,
                        x,
                        i,
                        zi_node=self._tk_object.sgchannels[i].node_info.path,
                        snapshot_cache=self._snapshot_cache,
                    )
                )
            # channel_list.lock()
            self.add_submodule("sgchannels", channel_list)

    def factory_reset(self, *, deep: bool = True) -> None:
        """Load the factory default settings.

        Args:
            deep: A flag that specifies if a synchronization
                should be performed between the device and the data
                server after loading the factory preset (default: True).
        """
        return self._tk_object.factory_reset(deep=deep)
