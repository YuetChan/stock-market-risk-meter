import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScoreChartComponent } from './score-oscillator.component';

describe('ScoreChartComponent', () => {
  let component: ScoreChartComponent;
  let fixture: ComponentFixture<ScoreChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ScoreChartComponent]
    });
    fixture = TestBed.createComponent(ScoreChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
