import { Component, Input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-star-evaluation',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './star-evaluation.component.html',
  styleUrl: './star-evaluation.component.scss'
})
export class StarEvaluationComponent {
  @Input() filledStars = 0;
  @Input() isInteractable = true;
  @Input() numberOfStars = 5;

  stars = Array(this.numberOfStars);

  clickStar(index: number) {
    if (!this.isInteractable) {
      return
    }
    this.filledStars = index + 1;
  }
}
