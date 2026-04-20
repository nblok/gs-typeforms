import { Box, Button, InputBase, Stack } from '@mui/material';

interface Props {
  formTitle: string;
  onFormTitleChange: (title: string) => void;
  onCancel: () => void;
  onPublish: () => void;
  publishing?: boolean;
}

export function BuilderTopBar({
  formTitle,
  onFormTitleChange,
  onCancel,
  onPublish,
  publishing = false,
}: Props) {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 1.5,
        px: 2.5,
        height: 52,
        bgcolor: 'background.paper',
        borderBottom: 1,
        borderColor: 'divider',
        flexShrink: 0,
      }}
    >
      <InputBase
        value={formTitle}
        onChange={(e) => onFormTitleChange(e.target.value)}
        inputProps={{ 'aria-label': 'Form title' }}
        sx={{
          fontSize: 15,
          fontWeight: 600,
          color: 'text.primary',
          flex: 1,
          maxWidth: 300,
        }}
      />
      <Box sx={{ flex: 1 }} />
      <Stack direction="row" spacing={1}>
        <Button
          onClick={onCancel}
          variant="outlined"
          size="small"
          disabled={publishing}
        >
          Cancel
        </Button>
        <Button
          onClick={onPublish}
          variant="contained"
          size="small"
          disabled={publishing}
        >
          {publishing ? 'Publishing…' : 'Publish'}
        </Button>
      </Stack>
    </Box>
  );
}
