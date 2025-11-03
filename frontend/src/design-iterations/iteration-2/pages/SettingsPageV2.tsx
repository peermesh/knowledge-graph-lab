import { ThemeProvider } from '../../shared/ThemeProvider'
import { SharedSettingsPage } from '../../shared/pages/SettingsPage'
import { iteration2Theme } from '../themeAdapter'

export function SettingsPageV2() {
  return (
    <ThemeProvider theme={iteration2Theme}>
      <SharedSettingsPage />
    </ThemeProvider>
  )
}

