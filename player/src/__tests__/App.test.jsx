import {render, screen, waitFor} from '@testing-library/react'
import '@testing-library/jest-dom'
import App from "../components/App";
import fetchMock from "jest-fetch-mock";
import {act} from "react-dom/test-utils";
import Channel from "../components/Channel";

beforeAll(() => {
    fetchMock.enableMocks();
    fetch.mockImplementation(() => Promise.resolve(
        new Response(JSON.stringify([
            {
                "id": 1,
                "name": "Main channel",
                "description": "We have implemented live streaming - enjoy!",
                "hls_path": "channel1"
            },
            {
                "id": 2,
                "name": "Jazz",
                "description": "The best local jazz music",
                "hls_path": "jazz/outputlist.m3u8"
            },
            {
                "id": 3,
                "name": "Bathroom",
                "description": "A perfect choice to enjoy your bathroom break",
                "hls_path": "bathroom/outputlist.m3u8"
            }
        ]))
    ));
});

afterAll(() => {
    fetchMock.disableMocks();
});

test('should load and display name', async () => {
    // given
    render(<App useLocalConfig={true}/>);

    // when then
    expect(screen.getByText("rAIdio")).toBeTruthy();
});

test('should display play/pause button', async () => {
    // given
    render(<App useLocalConfig={true}/>);

    // when
    const buttons = screen.getAllByRole("button");

    // then
    expect(buttons.length).toBeGreaterThan(0);
    expect(buttons[0]).toBeInTheDocument();
});

test('should generate all channels', async () => {
    // given
    // eslint-disable-next-line testing-library/no-unnecessary-act
    await act(async  () => {
        await render(<App useLocalConfig={true}/>);
    })

    // when then
    await waitFor(() => {
        const channels = screen.getAllByTestId("channel");
        expect(channels.length).toEqual(3);
    });
});

test('should render a channel', async () => {
    // given
    render(<Channel num={4} active={false} switchChannel={() => {}} hlsPath={""} thumbnailPath={""}/>);

    // when then
    expect(screen.getByText("4")).toBeInTheDocument();
});