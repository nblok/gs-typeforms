import type { SvgIconComponent } from '@mui/icons-material';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import NotesIcon from '@mui/icons-material/Notes';
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted';
import ToggleOnIcon from '@mui/icons-material/ToggleOn';
import StarIcon from '@mui/icons-material/Star';
import type { FieldType } from '../../types/fieldDefinition';

export interface FieldTypeMeta {
  color: string;
  Icon: SvgIconComponent;
}

export const FIELD_TYPE_META: Record<FieldType, FieldTypeMeta> = {
  short_text: { color: '#4F8EF7', Icon: TextFieldsIcon },
  long_text: { color: '#7B61FF', Icon: NotesIcon },
  multiple_choice: { color: '#F97316', Icon: FormatListBulletedIcon },
  yes_no: { color: '#10B981', Icon: ToggleOnIcon },
  rating: { color: '#F59E0B', Icon: StarIcon },
};
