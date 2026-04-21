import { Outlet } from 'react-router-dom';
import { AppBar, Box, Toolbar, Typography } from '@mui/material';
import { RespondentBadge } from '../../components/RespondentBadge';

export default function LayoutPage() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <AppBar position="static">
        <Toolbar sx={{ gap: 2 }}>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            TypeForms
          </Typography>
          <RespondentBadge />
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ flex: 1, overflow: 'auto' }}>
        <Outlet />
      </Box>
    </Box>
  );
}
