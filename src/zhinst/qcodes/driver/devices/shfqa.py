""" Autogenerated module for the SHFQA QCodes driver. """
from typing import Dict, List, Union
import numpy as np
from zhinst.toolkit import Waveforms
from zhinst.toolkit.interface import AveragingMode, SHFQAChannelMode
from zhinst.qcodes.driver.devices.base import ZIBaseInstrument
from zhinst.qcodes.qcodes_adaptions import ZINode, ZIChannelList


class Generator(ZINode):
    """Generator node

    Implements basic functionality of the generator allowing the user to write
    and upload their *'.seqC'* code.

    In contrast to other AWG Sequencers, e.g. from the HDAWG, SHFSG
    it does not provide writing access to the Waveform Memories
    and hence does not come with predefined waveforms such as `gauss`
    or `ones`. Therefore, all waveforms need to be defined in Python
    and uploaded to the device using `upload_waveforms` method.

    Args:
        root: Root of the nodetree
        tree: Tree (node path as tuple) of the current node
        daq_server: Instance of the ziDAQServer
        serial: Serial of the device.
        index: Index of the coresponding awg channel
        max_qubits_per_channel: Max qubits per channel
    """

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, f"generator", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object

    def enable_sequencer(self, *, single: bool) -> None:
        """Starts the sequencer.

        Args:
            single: Flag if the sequencer should be disabled after finishing
            execution.
        """
        return self._tk_object.enable_sequencer(single=single)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.005) -> None:
        """Wait until the generator execution is finished.

        Args:
            timeout: The maximum waiting time in seconds for the generator
                (default: 10).
            sleep_time: Time in seconds to wait between requesting generator
                state.

        Raises:
            RuntimeError: If continuous mode is enabled
            TimeoutError: If the sequencer program did not finish within the
                specified timeout time.
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def load_sequencer_program(
        self, sequencer_program: str, *, timeout: float = 10
    ) -> None:
        """Compiles and loads a sequencer program.

        Args:
            sequencer_program: Sequencer program to be uploaded
            timeout: Maximum time to wait for the compilation on the device in
                seconds. (default = 10s)

        Raises:
            TimeoutError: If the upload or compilation times out.
            RuntimeError: If the upload or compilation failed.
        """
        return self._tk_object.load_sequencer_program(
            sequencer_program=sequencer_program, timeout=timeout
        )

    def write_to_waveform_memory(
        self, pulses: Union[Waveforms, dict], *, clear_existing: bool = True
    ) -> None:
        """Writes pulses to the waveform memory.

        Args:
            pulses: Waveforms that should be uploaded.
            clear_existing: Flag whether to clear the waveform memory before the
                present upload. (default = True)
        """
        return self._tk_object.write_to_waveform_memory(
            pulses=pulses, clear_existing=clear_existing
        )

    def read_from_waveform_memory(self, slots: List[int] = None) -> Waveforms:
        """Read pulses from the waveform memory.

        Args:
            slots: List of waveform indexes to read from the device. If not
                specified all assigned waveforms will be downloaded.

        Returns:
            Mutuable mapping of the downloaded waveforms.
        """
        return self._tk_object.read_from_waveform_memory(slots=slots)

    def configure_sequencer_triggering(
        self, *, aux_trigger: str, play_pulse_delay: float = 0.0
    ) -> None:
        """Configure the sequencer triggering.

        Arguments:

            aux_trigger: Alias for the trigger source used in the sequencer.
                For the list of available values, use `available_aux_trigger_inputs`
            play_pulse_delay: Delay in seconds before the start of waveform playback.
        """
        return self._tk_object.configure_sequencer_triggering(
            aux_trigger=aux_trigger, play_pulse_delay=play_pulse_delay
        )

    @property
    def available_aux_trigger_inputs(self) -> List[str]:
        return self._tk_object.available_aux_trigger_inputs


class Readout(ZINode):
    """Readout node.

    Implements basic functionality of the readout, e.g allowing the user to
    write the integration weight.

    Args:
        root: Root of the nodetree
        tree: Tree (node path as tuple) of the current node
        daq_server: Instance of the ziDAQServer
        serial: Serial of the device.
        index: Index of the coresponding awg channel
        max_qubits_per_channel: Max qubits per channel
    """

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, f"readout", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object

    def configure_result_logger(
        self,
        *,
        result_source: str,
        result_length: int,
        num_averages: int = 1,
        averaging_mode: AveragingMode = AveragingMode.CYCLIC,
    ) -> None:
        """Configures the result logger for readout mode.

        Args:
            result_source: String-based tag to select the result source in readout
                mode, e.g. "result_of_integration" or "result_of_discrimination".
            result_length: Number of results to be returned by the result logger
            num_averages: Number of averages, will be rounded to 2^n
            averaging_mode: Select the averaging order of the result, with
                0 = cyclic and 1 = sequential.
        """
        return self._tk_object.configure_result_logger(
            result_source=result_source,
            result_length=result_length,
            num_averages=num_averages,
            averaging_mode=averaging_mode,
        )

    def run(self) -> None:
        """Reset and enable the result logger."""
        return self._tk_object.run()

    def stop(self, *, timeout: float = 10, sleep_time: float = 0.05) -> None:
        """Stop the result logger.

        Args:
            timeout: The maximum waiting time in seconds for the Readout
                (default: 10).
            sleep_time: Sleep interval in seconds. (default = 0.05)

        Raises:
            TimeoutError: The result logger could not been stopped within the
                given time.
        """
        return self._tk_object.stop(timeout=timeout, sleep_time=sleep_time)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.05) -> None:
        """Wait until the readout is finished.

        Args:
            timeout: The maximum waiting time in seconds for the Readout
                (default: 10).
            sleep_time: Sleep interval in seconds. (default = 0.05)

        Raises:
            TimeoutError: if the readout recording is not completed within the
                given time.
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def read(self, *, timeout: float = 10) -> np.array:
        """Waits until the logger finished recording and returns the measured data.

        Args:
            timeout: Maximum time to wait for data in seconds (default = 10s)

        Returns:
            Result logger data.
        """
        return self._tk_object.read(timeout=timeout)

    def write_integration_weights(
        self,
        weights: Union[Waveforms, dict],
        *,
        integration_delay: float = 0.0,
        clear_existing: bool = True,
    ) -> None:
        """Configures the weighted integration.

        Args:
            weights: Dictionary containing the complex weight vectors, where
                keys correspond to the indices of the integration units to be
                configured.
            integration_delay: Delay in seconds before starting the readout.
                (default = 0.0)
            clear_existing: Flag whether to clear the waveform memory before
                the present upload. (default = True)
        """
        return self._tk_object.write_integration_weights(
            weights=weights,
            integration_delay=integration_delay,
            clear_existing=clear_existing,
        )

    def read_integration_weights(self, slots: List[int] = None) -> Waveforms:
        """Read integration weights from the waveform memory.

        Args:
            slots: List of weight slots to read from the device. If not specfied
                all available weights will be downloaded.

        Returns:
            Mutuable mapping of the downloaded weights.
        """
        return self._tk_object.read_integration_weights(slots=slots)


class Spectroscopy(ZINode):
    """Spectroscopy node

    Implements basic functionality of the spectroscopy, e.g allowing the user to
    read the result logger data.

    Args:
        root: Root of the nodetree
        tree: Tree (node path as tuple) of the current node
        daq_server: Instance of the ziDAQServer
        serial: Serial of the device.
        index: Index of the coresponding awg channel
    """

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"spectroscopy",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object

    def configure_result_logger(
        self,
        *,
        result_length: int,
        num_averages: int = 1,
        averaging_mode: AveragingMode = AveragingMode.CYCLIC,
    ) -> None:
        """Configures the result logger for spectroscopy mode.

        Args:
            result_length: Number of results to be returned by the result logger
            num_averages: Number of averages, will be rounded to 2^n.
            averaging_mode: Averaging order of the result.
        """
        return self._tk_object.configure_result_logger(
            result_length=result_length,
            num_averages=num_averages,
            averaging_mode=averaging_mode,
        )

    def run(self) -> None:
        """Resets and enables the spectroscopy result logger."""
        return self._tk_object.run()

    def stop(self, *, timeout: float = 10, sleep_time: float = 0.05) -> None:
        """Stop the result logger.

        Args:
            timeout: The maximum waiting time in seconds for the
                Spectroscopy (default: 10).
            sleep_time: Time in seconds to wait between
                requesting Spectroscopy state
        Raises:
            TimeoutError: If the result logger could not been stopped within the
                given time.

        """
        return self._tk_object.stop(timeout=timeout, sleep_time=sleep_time)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.05) -> None:
        """Wait until spectroscopy is finished.

        Args:
            timeout (float): The maximum waiting time in seconds for the
                Spectroscopy (default: 10).
            sleep_time (float): Time in seconds to wait between
                requesting Spectroscopy state

        Raises:
            TimeoutError: if the spectroscopy recording is not completed within the
                given time.

        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def read(self, *, timeout: float = 10) -> np.array:
        """Waits until the logger finished recording and returns the measured data.

        Args:
            timeout: Maximum time to wait for data in seconds (default = 10s)

        Returns:
            An array containing the result logger data.

        """
        return self._tk_object.read(timeout=timeout)


class QAChannel(ZINode):
    """Quantum Analyser Channel for the SHFQA.

    :class:`QAChannel` implements basic functionality to configure QAChannel
    settings of the :class:`SHFQA` instrument.
    Besides the :class:`Generator`, :class:`Readout` and :class:`Sweeper`
    modules it also provides an easy access to commonly used `QAChannel` parameters.

    Args:
        device: SHFQA device object.
        session: Underlying session.
        tree: Node tree (node path as tuple) of the corresponding node.
    """

    def __init__(self, parent, tk_object, index, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"qachannel_{index}",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object

        if self._tk_object.generator:

            self.add_submodule(
                "generator",
                Generator(
                    self,
                    self._tk_object.generator,
                    zi_node=self._tk_object.generator.node_info.path,
                    snapshot_cache=self._snapshot_cache,
                ),
            )

        if self._tk_object.readout:

            self.add_submodule(
                "readout",
                Readout(
                    self,
                    self._tk_object.readout,
                    zi_node=self._tk_object.readout.node_info.path,
                    snapshot_cache=self._snapshot_cache,
                ),
            )

        if self._tk_object.spectroscopy:

            self.add_submodule(
                "spectroscopy",
                Spectroscopy(
                    self,
                    self._tk_object.spectroscopy,
                    zi_node=self._tk_object.spectroscopy.node_info.path,
                    snapshot_cache=self._snapshot_cache,
                ),
            )

    def configure_channel(
        self,
        *,
        input_range: int,
        output_range: int,
        center_frequency: float,
        mode: SHFQAChannelMode,
    ) -> None:
        """Configures the RF input and output of a specified channel.

        Args:
            input_range: Maximal range of the signal input power in dBm
            output_range: Maximal range of the signal output power in dBm
            center_frequency: Center frequency of the analysis band [Hz]
            mode: Select between spectroscopy and readout mode.
        """
        return self._tk_object.configure_channel(
            input_range=input_range,
            output_range=output_range,
            center_frequency=center_frequency,
            mode=mode,
        )


class SHFScope(ZINode):
    """SHFQA Scope Node

    Implements basic functionality of the scope node, e.g allowing the user to
    read the data.

    Args:
        root: Root of the nodetree
        tree: Tree (node path as tuple) of the current node
        daq_server: Instance of the ziDAQServer
        serial: Serial of the device.
    """

    def __init__(self, parent, tk_object, index, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"shfscope_{index}",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object

    def run(
        self, *, single: bool = True, timeout: float = 10, sleep_time: float = 0.005
    ) -> None:
        """Run the scope recording.

        Args:
            timeout: The maximum waiting time in seconds for the Scope
                (default = 10).
            sleep_time: Time in seconds to wait between requesting the progress
                and records values (default = 0.005).

        Raises:
            TimeoutError: The scope did not start within the specified
                timeout.
        """
        return self._tk_object.run(
            single=single, timeout=timeout, sleep_time=sleep_time
        )

    def stop(self, *, timeout: float = 10, sleep_time: float = 0.005) -> None:
        """Stop the scope recording.

        Args:
            timeout: The maximum waiting time in seconds for the scope
                (default = 10).
            sleep_time: Time in seconds to wait between requesting the progress
                and records values (default = 0.005).

        Raises:
            TimeoutError: The scope did not stop within the specified
                timeout.
        """
        return self._tk_object.stop(timeout=timeout, sleep_time=sleep_time)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.005) -> None:
        """Wait until the scope recording is finished.

        Args:
            timeout: The maximum waiting time in seconds for the Scope
                (default = 10).
            sleep_time: Time in seconds to wait between requesting the progress
                and records values (default = 0.005).

        Raises:
            TimeoutError: The scope did not finish within the specified
                timeout.
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def configure(
        self,
        *,
        input_select: Dict[int, str],
        num_samples: int,
        trigger_input: str,
        num_segments: int = 1,
        num_averages: int = 1,
        trigger_delay: float = 0,
    ) -> None:
        """Configures the scope for a measurement.

        Args:
            input_select: Map of a specific scope channel an their signal
                source, e.g. "channel0_signal_input". (For a list of available
                values use `available_inputs`)
            num_samples: Number samples to recorded in a scope shot.
            trigger_input: Specifies the trigger source of the scope
                acquisition - if set to None, the self-triggering mode of the
                scope becomes active, which is useful e.g. for the GUI.
                For a list of available trigger values use
                `available_trigger_inputs`.
            num_segments: Number of distinct scope shots to be returned after
                ending the acquisition.
            num_averages: Specifies how many times each segment should be
                averaged on hardware; to finish a scope acquisition, the number
                of issued triggers must be equal to num_segments * num_averages.
            trigger_delay: delay in samples specifying the time between the
                start of data acquisition and reception of a trigger.
        """
        return self._tk_object.configure(
            input_select=input_select,
            num_samples=num_samples,
            trigger_input=trigger_input,
            num_segments=num_segments,
            num_averages=num_averages,
            trigger_delay=trigger_delay,
        )

    def read(self, *, timeout: float = 10) -> tuple:
        """Read out the recorded data from the scope.

        Args:
            timeout: The maximum waiting time in seconds for the
                Scope (default: 10).

        Returns:
            (recorded_data, recorded_data_range, scope_time)

        Raises:
            TimeoutError: if the scope recording is not completed before
                timeout.
        """
        return self._tk_object.read(timeout=timeout)

    @property
    def available_trigger_inputs(self) -> List[str]:
        return self._tk_object.available_trigger_inputs

    @property
    def available_inputs(self) -> List[str]:
        return self._tk_object.available_inputs


class SHFQA(ZIBaseInstrument):
    """QCodes driver for the Zurich Instruments SHFQA."""

    def _init_additional_nodes(self):
        """init class specific modules and paramaters."""

        if self._tk_object.qachannels:

            channel_list = ZIChannelList(
                self,
                "qachannels",
                QAChannel,
                zi_node=self._tk_object.qachannels.node_info.path,
                snapshot_cache=self._snapshot_cache,
            )
            for i, x in enumerate(self._tk_object.qachannels):
                channel_list.append(
                    QAChannel(
                        self,
                        x,
                        i,
                        zi_node=self._tk_object.qachannels[i].node_info.path,
                        snapshot_cache=self._snapshot_cache,
                    )
                )
            # channel_list.lock()
            self.add_submodule("qachannels", channel_list)

        if self._tk_object.scopes:

            channel_list = ZIChannelList(
                self,
                "scopes",
                SHFScope,
                zi_node=self._tk_object.scopes.node_info.path,
                snapshot_cache=self._snapshot_cache,
            )
            for i, x in enumerate(self._tk_object.scopes):
                channel_list.append(
                    SHFScope(
                        self,
                        x,
                        i,
                        zi_node=self._tk_object.scopes[i].node_info.path,
                        snapshot_cache=self._snapshot_cache,
                    )
                )
            # channel_list.lock()
            self.add_submodule("scopes", channel_list)

    def factory_reset(self, *, deep: bool = True) -> None:
        """Load the factory default settings.

        Args:
            deep: A flag that specifies if a synchronisation
                should be performed between the device and the data
                server after loading the factory preset (default: True).
        """
        return self._tk_object.factory_reset(deep=deep)

    def start_continuous_sw_trigger(
        self, *, num_triggers: int, wait_time: float
    ) -> None:
        """Issues a specified number of software triggers.

        Issues a specified number of software triggers with a certain wait time
        in between. The function guarantees reception and proper processing of
        all triggers by the device, but the time between triggers is
        non-deterministic by nature of software triggering. Only use this
        function for prototyping and/or cases without strong timing requirements.

        Args:
            num_triggers: Number of triggers to be issued
            wait_time: Time between triggers in seconds
        """
        return self._tk_object.start_continuous_sw_trigger(
            num_triggers=num_triggers, wait_time=wait_time
        )

    @property
    def max_qubits_per_channel(self) -> int:
        return self._tk_object.max_qubits_per_channel
