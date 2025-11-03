import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedSettingsPage } from '../../shared/pages/SettingsPage'
import { iteration1Theme } from '../themeAdapter'

export function SettingsPageV1() {
  return (
    <ThemeProvider theme={iteration1Theme}>
      <SharedSettingsPage />
    </ThemeProvider>
  )
}

