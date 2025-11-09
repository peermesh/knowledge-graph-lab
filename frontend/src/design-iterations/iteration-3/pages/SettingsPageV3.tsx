import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedSettingsPage } from '../../shared/pages/SettingsPage'
import { iteration3Theme } from '../themeAdapter'

export function SettingsPageV3() {
  return (
    <ThemeProvider theme={iteration3Theme}>
      <SharedSettingsPage />
    </ThemeProvider>
  )
}












