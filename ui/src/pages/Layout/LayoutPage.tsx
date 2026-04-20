import { Outlet } from 'react-router-dom';
import { AppBar, Box, Toolbar, Typography } from '@mui/material';

export default function LayoutPage() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">TypeForms</Typography>
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ flex: 1, overflow: 'auto' }}>
        <Outlet />
      </Box>
    </Box>
  );
}
