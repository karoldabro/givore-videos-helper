# ElevenLabs Configuration

Voice and audio generation settings for Givore content.

## Voice Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Voice ID | `HIYif4jehvc9P9A8DYbX` | Pablo - Deep, Confident and Clear |
| Model | `eleven_multilingual_v2` | Best for Spanish content |
| Language | `es` | Spanish |

## Voice Settings

| Parameter | Value | Range |
|-----------|-------|-------|
| `stability` | `0.35` | 0.0 - 1.0 (35%) |
| `similarity_boost` | `0.4` | 0.0 - 1.0 (40%) |
| `style` | `0.3` | 0.0 - 1.0 (30%) |
| `use_speaker_boost` | `true` | boolean |
| `speed` | `1.06` | 0.7 - 1.2 |

## Output Settings

| Setting | Value |
|---------|-------|
| Format | `mp3_44100_128` |
| Output Directory | `projects/[folder]/` |

## MCP Tool Call Example

```
text_to_speech(
  text=[script content],
  voice_id="HIYif4jehvc9P9A8DYbX",
  model_id="eleven_multilingual_v2",
  language="es",
  stability=0.35,
  similarity_boost=0.4,
  style=0.3,
  use_speaker_boost=true,
  speed=1.06,
  output_directory="projects/[date]_[topic]/",
  output_format="mp3_44100_128"
)
```

## Setup Requirements

ElevenLabs MCP server must be configured in Claude Code:

```json
{
  "mcpServers": {
    "ElevenLabs": {
      "command": "uvx",
      "args": ["elevenlabs-mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "${ELEVENLABS_API_KEY}",
        "ELEVENLABS_MCP_BASE_PATH": "/media/kdabrow/Programy/givore/projects"
      }
    }
  }
}
```

Environment variable required: `ELEVENLABS_API_KEY`
