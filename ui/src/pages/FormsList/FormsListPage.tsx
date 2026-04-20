import { Box, Button, Container, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

export default function FormsListPage() {
  return (
    <Container maxWidth="lg">
      <Box>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            my: 2,
          }}
        >
          <Typography variant="h4">My Forms</Typography>
          <Box>
            <Button component={RouterLink} variant="contained" to="/builder">
              Create Form
            </Button>
          </Box>
        </Box>
      </Box>
    </Container>
  );
}
