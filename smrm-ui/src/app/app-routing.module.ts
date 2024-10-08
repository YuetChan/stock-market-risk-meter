import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ScoreOscillatorComponent } from './score-oscillator/score-oscillator.component'; // Adjust the import path as necessary

const routes: Routes = [
  { path: '', component: ScoreOscillatorComponent } // Route for the home page
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
